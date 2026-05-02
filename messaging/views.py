from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Message
from missions.models import Mission
from notifications.utils import create_notification


def _can_access_conversation(user, mission):
    return user == mission.client or user == mission.selected_student


@login_required
def conversation(request, mission_pk):
    mission = get_object_or_404(Mission, pk=mission_pk)
    if not _can_access_conversation(request.user, mission):
        return redirect('mission_detail', pk=mission_pk)
    messages_qs = mission.messages.select_related('sender')
    mission.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    other_user = mission.selected_student if request.user == mission.client else mission.client
    return render(request, 'messaging/conversation.html', {
        'mission': mission,
        'messages': messages_qs,
        'other_user': other_user,
    })


@login_required
def send_message(request, mission_pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    mission = get_object_or_404(Mission, pk=mission_pk)
    if not _can_access_conversation(request.user, mission):
        return JsonResponse({'error': 'Forbidden'}, status=403)
    content = request.POST.get('content', '').strip()
    if not content:
        return JsonResponse({'error': 'Message vide'}, status=400)
    msg = Message.objects.create(mission=mission, sender=request.user, content=content)
    other = mission.selected_student if request.user == mission.client else mission.client
    create_notification(
        user=other,
        notif_type='message',
        title='Nouveau message',
        message=f'{request.user.get_full_name()} vous a envoye un message.',
        link=f'/messages/{mission_pk}/',
    )
    return JsonResponse({
        'id': msg.pk,
        'sender': request.user.get_full_name() or request.user.username,
        'content': msg.content,
        'sent_at': msg.sent_at.strftime('%H:%M'),
        'is_me': True,
    })


@login_required
def poll_messages(request, mission_pk):
    mission = get_object_or_404(Mission, pk=mission_pk)
    if not _can_access_conversation(request.user, mission):
        return JsonResponse({'error': 'Forbidden'}, status=403)
    since_id = request.GET.get('since', 0)
    new_msgs = mission.messages.filter(pk__gt=since_id).exclude(sender=request.user)
    new_msgs.filter(is_read=False).update(is_read=True)
    data = [
        {
            'id': m.pk,
            'sender': m.sender.get_full_name() or m.sender.username,
            'content': m.content,
            'sent_at': m.sent_at.strftime('%H:%M'),
            'is_me': False,
        }
        for m in new_msgs
    ]
    return JsonResponse({'messages': data})
