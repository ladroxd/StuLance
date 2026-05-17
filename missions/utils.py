from django.core.cache import cache
from .models import Category

CATEGORY_CACHE_KEY = 'all_categories'
CATEGORY_CACHE_TTL = 60 * 15  # 15 minutes


def get_all_categories():
    cats = cache.get(CATEGORY_CACHE_KEY)
    if cats is None:
        cats = list(Category.objects.all())
        cache.set(CATEGORY_CACHE_KEY, cats, CATEGORY_CACHE_TTL)
    return cats


def invalidate_category_cache():
    cache.delete(CATEGORY_CACHE_KEY)
