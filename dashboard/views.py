from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from missions.models import Mission, Application


@login_required
def dashboard(request):
    user = request.user
    if user.is_student():
        applications = Application.objects.filter(student=user).select_related('mission', 'mission__client')
        active_missions = Mission.objects.filter(selected_student=user, status='in_progress')
        completed_missions = Mission.objects.filter(selected_student=user, status='completed')
        profile = user.student_profile
        context = {
            'applications': applications,
            'active_missions': active_missions,
            'completed_missions': completed_missions,
            'profile': profile,
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
