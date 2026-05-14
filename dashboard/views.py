from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg
from missions.models import Mission, Application, Review, Submission
from accounts.models import User, StudentProfile
from gigs.models import Gig


@login_required
def dashboard(request):
    user = request.user
    if user.is_student():
        applications = Application.objects.filter(student=user).select_related('mission', 'mission__client')
        active_missions = Mission.objects.filter(selected_student=user, status='in_progress')
        completed_missions = Mission.objects.filter(selected_student=user, status='completed')
        total_earnings = completed_missions.aggregate(total=Sum('budget'))['total'] or 0
        profile = user.student_profile
        my_gigs = Gig.objects.filter(student=user)
        # Missions where recruiter accepted the submission but admin hasn't approved yet
        funds_on_hold = Submission.objects.filter(
            student=user,
            status=Submission.STATUS_ACCEPTED,
            mission__status='in_progress',
        ).select_related('mission')
        funds_on_hold_total = sum(s.mission.budget for s in funds_on_hold)
        context = {
            'applications': applications,
            'active_missions': active_missions,
            'completed_missions': completed_missions,
            'total_earnings': total_earnings,
            'profile': profile,
            'my_gigs': my_gigs,
            'funds_on_hold': funds_on_hold,
            'funds_on_hold_total': funds_on_hold_total,
        }
        return render(request, 'dashboard/student.html', context)
    elif user.is_client():
        missions = Mission.objects.filter(client=user).prefetch_related('applications')
        context = {
            'open_missions': missions.filter(status='open'),
            'in_progress_missions': missions.filter(status='in_progress'),
            'completed_missions': missions.filter(status='completed'),
            'profile': user.client_profile,
        }
        return render(request, 'dashboard/client.html', context)
    return redirect('home')


@staff_member_required
def admin_stats(request):
    total_students = User.objects.filter(role='student').count()
    total_clients = User.objects.filter(role='client').count()
    total_missions = Mission.objects.count()
    open_missions = Mission.objects.filter(status='open').count()
    in_progress_missions = Mission.objects.filter(status='in_progress').count()
    completed_missions = Mission.objects.filter(status='completed').count()
    total_applications = Application.objects.count()
    total_reviews = Review.objects.count()
    avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
    total_budget_completed = Mission.objects.filter(status='completed').aggregate(total=Sum('budget'))['total'] or 0
    verified_students = StudentProfile.objects.filter(verification_status='verified').count()
    pending_verifications = StudentProfile.objects.filter(verification_status='pending').count()

    from missions.models import Category
    top_categories = Category.objects.annotate(mission_count=Count('missions')).order_by('-mission_count')[:5]

    context = {
        'total_students': total_students,
        'total_clients': total_clients,
        'total_missions': total_missions,
        'open_missions': open_missions,
        'in_progress_missions': in_progress_missions,
        'completed_missions': completed_missions,
        'total_applications': total_applications,
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating, 2),
        'total_budget_completed': total_budget_completed,
        'verified_students': verified_students,
        'pending_verifications': pending_verifications,
        'top_categories': top_categories,
    }
    return render(request, 'dashboard/admin_stats.html', context)
