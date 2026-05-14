from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Message, DirectConversation, DirectMessage
from missions.models import Mission
from notifications.utils import create_notification

User = get_user_model()


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


# ── Direct Messaging ──────────────────────────────────────────────────────────

@login_required
def inbox(request):
    convs = DirectConversation.objects.filter(
        participant1=request.user
    ) | DirectConversation.objects.filter(
        participant2=request.user
    )
    convs = convs.order_by('-updated_at').select_related('participant1', 'participant2')

    conversations = []
    for conv in convs:
        other = conv.other_participant(request.user)
        last_msg = conv.direct_messages.last()
        conversations.append({
            'conv': conv,
            'other': other,
            'last_msg': last_msg,
            'unread': conv.unread_count(request.user),
        })

    return render(request, 'messaging/inbox.html', {'conversations': conversations})


@login_required
def start_conversation(request, user_pk):
    """GET — get or create a direct conversation with user_pk and redirect to it."""
    recipient = get_object_or_404(User, pk=user_pk)
    if recipient == request.user:
        return redirect('inbox')
    conv = DirectConversation.get_or_create_between(request.user, recipient)
    return redirect('direct_conversation', pk=conv.pk)


@login_required
def new_conversation(request):
    if request.method == 'POST':
        query = request.POST.get('recipient', '').strip()
        try:
            recipient = User.objects.get(username=query) if '@' not in query else User.objects.get(email=query)
        except User.DoesNotExist:
            django_messages.error(request, 'No user found with that username or email.')
            return redirect('inbox')

        if recipient == request.user:
            django_messages.error(request, 'You cannot message yourself.')
            return redirect('inbox')

        conv = DirectConversation.get_or_create_between(request.user, recipient)
        return redirect('direct_conversation', pk=conv.pk)

    return redirect('inbox')


@login_required
def direct_conversation(request, pk):
    conv = get_object_or_404(DirectConversation, pk=pk)
    if request.user not in (conv.participant1, conv.participant2):
        return redirect('inbox')

    conv.direct_messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    msgs = conv.direct_messages.select_related('sender')
    other = conv.other_participant(request.user)

    return render(request, 'messaging/direct_conversation.html', {
        'conv': conv,
        'messages': msgs,
        'other': other,
    })


@login_required
def direct_send(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    conv = get_object_or_404(DirectConversation, pk=pk)
    if request.user not in (conv.participant1, conv.participant2):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    content = request.POST.get('content', '').strip()
    if not content:
        return JsonResponse({'error': 'Empty message'}, status=400)

    msg = DirectMessage.objects.create(conversation=conv, sender=request.user, content=content)
    conv.save()  # bump updated_at

    other = conv.other_participant(request.user)
    create_notification(
        user=other,
        notif_type='message',
        title='New message',
        message=f'{request.user.get_full_name() or request.user.username} sent you a message.',
        link=f'/messages/{conv.pk}/chat/',
    )

    return JsonResponse({
        'id': msg.pk,
        'sender': request.user.get_full_name() or request.user.username,
        'content': msg.content,
        'sent_at': msg.sent_at.strftime('%H:%M'),
        'is_me': True,
    })


@login_required
def direct_poll(request, pk):
    conv = get_object_or_404(DirectConversation, pk=pk)
    if request.user not in (conv.participant1, conv.participant2):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    since_id = request.GET.get('since', 0)
    new_msgs = conv.direct_messages.filter(pk__gt=since_id).exclude(sender=request.user)
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


@login_required
def delete_conversation(request, pk):
    if request.method == 'POST':
        conv = get_object_or_404(DirectConversation, pk=pk)
        if request.user in (conv.participant1, conv.participant2):
            conv.delete()
    return redirect('inbox')
