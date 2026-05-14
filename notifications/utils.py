from .models import Notification


def create_notification(user, notif_type, title_key, message_key, params=None, link=''):
    """Create a notification storing translation keys + params.

    title_key / message_key must match a key in notifications.translation_keys.
    params is a plain dict of string values used to fill the message template
    (e.g. {'name': 'Ali Hassan', 'mission': 'Build a website'}).
    """
    Notification.objects.create(
        user=user,
        notif_type=notif_type,
        title_key=title_key,
        message_key=message_key,
        params=params or {},
        link=link,
    )
