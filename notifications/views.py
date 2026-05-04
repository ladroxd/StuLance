from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification


@login_required
def notification_list(request):
    notifs = Notification.objects.filter(user=request.user)

    # Group stacked notifications by (type, link) — keeps ordering by latest
    seen = {}
    grouped = []
    for n in notifs:
        key = (n.notif_type, n.link)
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
    return render(request, 'notifications/list.html', {'grouped': grouped})


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
def unread_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})


@login_required
def recent_notifications(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    data = [
        {
            'id': n.pk,
            'title': n.title,
            'message': n.message[:80] + ('…' if len(n.message) > 80 else ''),
            'link': n.link,
            'is_read': n.is_read,
            'notif_type': n.notif_type,
        }
        for n in notifs
    ]
    unread = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'notifications': data, 'unread': unread})
