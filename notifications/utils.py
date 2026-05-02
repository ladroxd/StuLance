from .models import Notification

def create_notification(user, notif_type, title, message, link=''):
    Notification.objects.create(
        user=user,
        notif_type=notif_type,
        title=title,
        message=message,
        link=link,
    )
