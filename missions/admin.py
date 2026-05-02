from django.contrib import admin
from .models import Mission, Application, Review, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'category', 'budget', 'status', 'created_at']
    list_filter = ['status', 'category']
    search_fields = ['title', 'description']
    actions = ['cancel_missions']

    @admin.action(description='Annuler les missions selectionnees')
    def cancel_missions(self, request, queryset):
        queryset.update(status='cancelled')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'mission', 'status', 'applied_at']
    list_filter = ['status']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'reviewee', 'mission', 'rating', 'created_at']
    list_filter = ['rating']
