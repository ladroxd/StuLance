import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.text import Truncator
from .models import Mission, Application, Review, Category, Report, Submission
from .forms import MissionForm, ApplicationForm, ReviewForm, SubmissionForm
from notifications.utils import create_notification


def mission_list(request):
    qs = Mission.objects.filter(status='open').select_related('client', 'client__client_profile', 'category')
    q = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    budget_min = request.GET.get('budget_min', '')
    budget_max = request.GET.get('budget_max', '')
    duration = request.GET.get('duration', '')

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(skills_required__icontains=q))
    if category_id:
        qs = qs.filter(category_id=category_id)
    if budget_min:
        qs = qs.filter(budget__gte=budget_min)
    if budget_max:
        qs = qs.filter(budget__lte=budget_max)
    if duration:
        qs = qs.filter(deadline_days__lte=duration)

    categories = Category.objects.all()

    missions_json = json.dumps([
        {
            'pk': m.pk,
            'title': m.title,
            'description': Truncator(m.description).words(20),
            'category': str(m.category) if m.category else '',
            'budget': float(m.budget),
            'deadline_days': m.deadline_days,
            'applications_count': m.applications.count(),
            'skills': [s.strip() for s in (m.skills_required or '').split(',') if s.strip()][:3],
            'company_name': (
                m.client.client_profile.company_name
                or m.client.get_full_name()
                or m.client.username
            ) if hasattr(m.client, 'client_profile') else m.client.username,
        }
        for m in qs
    ], ensure_ascii=False)

    return render(request, 'missions/list.html', {
        'missions': qs,
        'missions_json': missions_json,
        'categories': categories,
        'q': q,
    })


def mission_detail(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    has_applied = False
    user_application = None
    submission = None
    submission_form = None
    if request.user.is_authenticated and request.user.is_student():
        user_application = Application.objects.filter(mission=mission, student=request.user).first()
        has_applied = user_application is not None
        if mission.status == 'in_progress' and mission.selected_student == request.user:
            submission = mission.submissions.first()
            if not submission or submission.status == 'revision':
                submission_form = SubmissionForm()
    submissions = mission.submissions.select_related('student') if request.user.is_authenticated and request.user == mission.client else None
    reviews = mission.reviews.select_related('reviewer')
    return render(request, 'missions/detail.html', {
        'mission': mission,
        'has_applied': has_applied,
        'user_application': user_application,
        'submission': submission,
        'submission_form': submission_form,
        'submissions': submissions,
        'reviews': reviews,
    })


@login_required
def mission_create(request):
    if not request.user.is_client():
        messages.error(request, 'Seuls les clients peuvent publier des missions.')
        return redirect('mission_list')
    if request.method == 'POST':
        form = MissionForm(request.POST)
        if form.is_valid():
            mission = form.save(commit=False)
            mission.client = request.user
            mission.save()
            messages.success(request, 'Mission publiee avec succes.')
            return redirect('mission_detail', pk=mission.pk)
    else:
        form = MissionForm()
    return render(request, 'missions/form.html', {'form': form, 'action': 'Publier'})


@login_required
def mission_edit(request, pk):
    mission = get_object_or_404(Mission, pk=pk, client=request.user)
    if request.method == 'POST':
        form = MissionForm(request.POST, instance=mission)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mission mise a jour.')
            return redirect('mission_detail', pk=pk)
    else:
        form = MissionForm(instance=mission)
    return render(request, 'missions/form.html', {'form': form, 'action': 'Modifier'})


@login_required
def mission_delete(request, pk):
    mission = get_object_or_404(Mission, pk=pk, client=request.user)
    if request.method == 'POST':
        mission.delete()
        messages.success(request, 'Mission supprimee.')
        return redirect('dashboard')
    return render(request, 'missions/confirm_delete.html', {'mission': mission})


@login_required
def apply_mission(request, pk):
    mission = get_object_or_404(Mission, pk=pk, status='open')
    if not request.user.is_student():
        messages.error(request, 'Seuls les etudiants peuvent postuler.')
        return redirect('mission_detail', pk=pk)
    if Application.objects.filter(mission=mission, student=request.user).exists():
        messages.warning(request, 'Vous avez deja postule a cette mission.')
        return redirect('mission_detail', pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.mission = mission
            app.student = request.user
            app.save()
            create_notification(
                user=mission.client,
                notif_type='application',
                title='Nouvelle candidature',
                message=f'{request.user.get_full_name()} a postule a votre mission "{mission.title}"',
                link=f'/missions/{mission.pk}/applications/',
            )
            messages.success(request, 'Candidature envoyee.')
            return redirect('mission_detail', pk=pk)
    else:
        form = ApplicationForm()
    return render(request, 'missions/apply.html', {'form': form, 'mission': mission})


@login_required
def mission_applications(request, pk):
    mission = get_object_or_404(Mission, pk=pk, client=request.user)
    applications = mission.applications.select_related('student', 'student__student_profile')
    return render(request, 'missions/applications.html', {'mission': mission, 'applications': applications})


@login_required
def accept_application(request, pk):
    application = get_object_or_404(Application, pk=pk, mission__client=request.user)
    if request.method == 'POST':
        application.status = 'accepted'
        application.save()
        mission = application.mission
        mission.status = 'in_progress'
        mission.selected_student = application.student
        mission.save()
        Application.objects.filter(mission=mission).exclude(pk=pk).update(status='rejected')
        create_notification(
            user=application.student,
            notif_type='mission_accepted',
            title='Candidature acceptee',
            message=f'Votre candidature pour "{mission.title}" a ete acceptee !',
            link=f'/missions/{mission.pk}/',
        )
        messages.success(request, 'Candidature acceptee. Mission en cours.')
    return redirect('mission_applications', pk=application.mission.pk)


@login_required
def reject_application(request, pk):
    application = get_object_or_404(Application, pk=pk, mission__client=request.user)
    if request.method == 'POST':
        application.status = 'rejected'
        application.save()
        messages.success(request, 'Candidature refusee.')
    return redirect('mission_applications', pk=application.mission.pk)


@login_required
def complete_mission(request, pk):
    mission = get_object_or_404(Mission, pk=pk, client=request.user, status='in_progress')
    if request.method == 'POST':
        mission.status = 'completed'
        mission.save()
        if mission.selected_student:
            profile = mission.selected_student.student_profile
            profile.total_missions += 1
            profile.save()
            create_notification(
                user=mission.selected_student,
                notif_type='mission_completed',
                title='Mission terminee',
                message=f'La mission "{mission.title}" a ete marquee comme terminee.',
                link=f'/missions/{mission.pk}/review/',
            )
        messages.success(request, 'Mission cloturee.')
        return redirect('leave_review', pk=pk)
    return render(request, 'missions/complete_confirm.html', {'mission': mission})


@login_required
def leave_review(request, pk):
    mission = get_object_or_404(Mission, pk=pk, status='completed')
    already_reviewed = Review.objects.filter(mission=mission, reviewer=request.user).exists()
    if already_reviewed:
        messages.info(request, 'Vous avez deja laisse un avis.')
        return redirect('mission_detail', pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.mission = mission
            review.reviewer = request.user
            review.reviewee = mission.selected_student if request.user == mission.client else mission.client
            review.save()
            _update_rating(review.reviewee)
            messages.success(request, 'Avis enregistre.')
            return redirect('mission_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'missions/review_form.html', {'form': form, 'mission': mission})


@login_required
def report_mission(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    if mission.client == request.user:
        messages.error(request, 'Vous ne pouvez pas signaler votre propre mission.')
        return redirect('mission_detail', pk=pk)
    if Report.objects.filter(reporter=request.user, reported_mission=mission).exists():
        messages.warning(request, 'Vous avez deja signale cette mission.')
        return redirect('mission_detail', pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        description = request.POST.get('description', '')
        if reason in dict(Report.REASON_CHOICES):
            Report.objects.create(
                reporter=request.user,
                reported_mission=mission,
                reason=reason,
                description=description,
            )
            messages.success(request, 'Signalement envoye. Notre equipe examinera cette mission.')
        return redirect('mission_detail', pk=pk)
    return render(request, 'missions/report_form.html', {
        'target_label': mission.title,
        'reasons': Report.REASON_CHOICES,
        'cancel_url': f'/missions/{pk}/',
        'submit_url': f'/missions/{pk}/report/',
    })


@login_required
def report_user(request, pk):
    from accounts.models import User as UserModel
    reported = get_object_or_404(UserModel, pk=pk)
    if reported == request.user:
        messages.error(request, 'Vous ne pouvez pas vous signaler vous-meme.')
        return redirect('home')
    if Report.objects.filter(reporter=request.user, reported_user=reported).exists():
        messages.warning(request, 'Vous avez deja signale cet utilisateur.')
        return redirect('home')
    if request.method == 'POST':
        reason = request.POST.get('reason')
        description = request.POST.get('description', '')
        if reason in dict(Report.REASON_CHOICES):
            Report.objects.create(
                reporter=request.user,
                reported_user=reported,
                reason=reason,
                description=description,
            )
            messages.success(request, 'Signalement envoye. Notre equipe examinera ce profil.')
        cancel = request.POST.get('cancel_url', '/')
        return redirect(cancel)
    cancel_url = request.META.get('HTTP_REFERER', '/')
    return render(request, 'missions/report_form.html', {
        'target_label': reported.get_full_name() or reported.username,
        'reasons': Report.REASON_CHOICES,
        'cancel_url': cancel_url,
        'submit_url': f'/missions/report-user/{pk}/',
    })


@login_required
def submit_mission(request, pk):
    mission = get_object_or_404(Mission, pk=pk, status='in_progress', selected_student=request.user)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.mission = mission
            sub.student = request.user
            sub.status = Submission.STATUS_PENDING
            sub.save()
            create_notification(
                user=mission.client,
                notif_type='submission',
                title='Nouvelle livraison',
                message=f'{request.user.get_full_name()} a soumis une livraison pour "{mission.title}"',
                link=f'/missions/{mission.pk}/',
            )
            messages.success(request, 'Livraison envoyee au client.')
    return redirect('mission_detail', pk=pk)


@login_required
def accept_submission(request, pk):
    submission = get_object_or_404(Submission, pk=pk, mission__client=request.user)
    if request.method == 'POST':
        submission.status = Submission.STATUS_ACCEPTED
        submission.save()
        create_notification(
            user=submission.student,
            notif_type='submission_accepted',
            title='Livraison acceptee',
            message=f'Votre livraison pour "{submission.mission.title}" a ete acceptee !',
            link=f'/missions/{submission.mission.pk}/',
        )
        messages.success(request, 'Livraison acceptee.')
    return redirect('mission_detail', pk=submission.mission.pk)


@login_required
def request_revision(request, pk):
    submission = get_object_or_404(Submission, pk=pk, mission__client=request.user)
    if request.method == 'POST':
        submission.status = Submission.STATUS_REVISION
        submission.save()
        create_notification(
            user=submission.student,
            notif_type='submission_revision',
            title='Revision demandee',
            message=f'Le client a demande une revision pour "{submission.mission.title}".',
            link=f'/missions/{submission.mission.pk}/',
        )
        messages.warning(request, 'Revision demandee.')
    return redirect('mission_detail', pk=submission.mission.pk)


def _update_rating(user):
    reviews = user.reviews_received.all()
    if reviews.exists():
        avg = sum(r.rating for r in reviews) / reviews.count()
        if user.is_student():
            user.student_profile.average_rating = round(avg, 2)
            user.student_profile.save()
        elif user.is_client():
            user.client_profile.average_rating = round(avg, 2)
            user.client_profile.save()
