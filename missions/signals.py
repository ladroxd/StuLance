from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Category
from .utils import invalidate_category_cache


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def clear_category_cache(sender, **kwargs):
    invalidate_category_cache()
