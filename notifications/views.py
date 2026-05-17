import json
import time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, StreamingHttpResponse
from .models import Notification
from .translation_keys import TITLES, MESSAGES, resolve


@login_required
def notification_list(request):
    notifs = Notification.objects.filter(user=request.user)

    # Group stacked notifications by (type, link) — keeps ordering by latest
    seen = {}
    grouped = []
    for n in notifs:
        key = (n.notif_type, n.link)
        # Resolve translated text now (request language is active at this point)
        if n.title_key:
            n.title = resolve(TITLES, n.title_key, n.params)
        if n.message_key:
            n.message = resolve(MESSAGES, n.message_key, n.params)
        if key in seen:
            entry = seen[key]
            entry['count'] += 1
            if not n.is_read:
                entry['has_unread'] = True
        else:
            entry = {'notif': n, 'count': 1, 'has_unread': not n.is_read}
            seen[key] = entry
            grouped.append(entry)

    notifs.filter(is_read=False).update(is_read=True)
    page_obj = Paginator(grouped, 30).get_page(request.GET.get('page'))
    return render(request, 'notifications/list.html', {'grouped': page_obj, 'page_obj': page_obj})


@login_required
def mark_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.link:
        return redirect(notif.link)
    return redirect('notification_list')


@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notification_list')


@login_required
def notification_stream(request):
    def event_stream(user_id):
        last_count = None
        last_id = None
        deadline = time.time() + 55  # reconnect every ~55s; frees dev server threads
        while time.time() < deadline:
            try:
                unread = Notification.objects.filter(user_id=user_id, is_read=False).count()
                latest = Notification.objects.filter(user_id=user_id).order_by('-pk').first()
                latest_id = latest.pk if latest else None

                if last_count is None:
                    payload = json.dumps({'unread': unread, 'new': False})
                    yield f'data: {payload}\n\n'
                elif unread > last_count or (latest_id and latest_id != last_id):
                    payload = json.dumps({'unread': unread, 'new': True})
                    yield f'data: {payload}\n\n'
                elif unread != last_count:
                    payload = json.dumps({'unread': unread, 'new': False})
                    yield f'data: {payload}\n\n'

                last_count = unread
                last_id = latest_id
                time.sleep(2)
            except Exception:
                break

    response = StreamingHttpResponse(
        event_stream(request.user.pk),
        content_type='text/event-stream',
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response


@login_required
def unread_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})


@login_required
def recent_notifications(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]

    def _title(n):
        if n.title_key:
            return resolve(TITLES, n.title_key, n.params)
        return n.title  # legacy

    def _message(n):
        if n.message_key:
            msg = resolve(MESSAGES, n.message_key, n.params)
            return msg[:80] + ('…' if len(msg) > 80 else '')
        msg = n.message
        return msg[:80] + ('…' if len(msg) > 80 else '')  # legacy

    data = [
        {
            'id': n.pk,
            'title': _title(n),
            'message': _message(n),
            'link': n.link,
            'is_read': n.is_read,
            'notif_type': n.notif_type,
        }
        for n in notifs
    ]
    unread = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'notifications': data, 'unread': unread})
