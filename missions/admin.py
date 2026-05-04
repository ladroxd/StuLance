from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Mission, Application, Review, Category, Report


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['icon_preview', 'name']
    search_fields = ['name']

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<i class="bi bi-{}"></i> {}', obj.icon, obj.icon)
        return '—'
    icon_preview.short_description = 'Icon'


class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    readonly_fields = ['student', 'cover_letter', 'status', 'applied_at']
    fields = ['student', 'status', 'applied_at']
    can_delete = False
    show_change_link = True


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'category', 'budget_display', 'status_badge', 'applications_count', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'description', 'client__username']
    readonly_fields = ['created_at', 'updated_at', 'applications_count']
    list_per_page = 20
    date_hierarchy = 'created_at'
    inlines = [ApplicationInline]
    actions = ['cancel_missions', 'reopen_missions']
    fieldsets = (
        ('Mission Info', {'fields': ('title', 'description', 'category', 'skills_required')}),
        ('Details', {'fields': ('client', 'budget', 'deadline_days', 'status', 'selected_student')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def budget_display(self, obj):
        return format_html('<strong style="color:#198754">{} MAD</strong>', obj.budget)
    budget_display.short_description = 'Budget'

    def status_badge(self, obj):
        colors = {
            'open':        ('#198754', 'Open'),
            'in_progress': ('#ffc107', 'In Progress'),
            'completed':   ('#0d6efd', 'Completed'),
            'cancelled':   ('#dc3545', 'Cancelled'),
        }
        color, label = colors.get(obj.status, ('#6c757d', obj.status))
        text = '#000' if obj.status == 'in_progress' else '#fff'
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600">{}</span>',
            color, text, label
        )
    status_badge.short_description = 'Status'

    def applications_count(self, obj):
        count = obj.applications.count()
        return format_html('<span style="font-weight:600">{}</span>', count)
    applications_count.short_description = 'Applications'

    @admin.action(description='✘ Cancel selected missions')
    def cancel_missions(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} mission(s) cancelled.')

    @admin.action(description='✔ Reopen selected missions')
    def reopen_missions(self, request, queryset):
        updated = queryset.filter(status='cancelled').update(status='open')
        self.message_user(request, f'{updated} mission(s) reopened.')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'mission', 'status_badge', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['student__username', 'mission__title']
    readonly_fields = ['applied_at']
    list_per_page = 25
    date_hierarchy = 'applied_at'
    actions = ['accept_applications', 'reject_applications']

    def status_badge(self, obj):
        colors = {
            'pending':  ('#ffc107', '⏳ Pending'),
            'accepted': ('#198754', '✔ Accepted'),
            'rejected': ('#dc3545', '✘ Rejected'),
        }
        color, label = colors.get(obj.status, ('#6c757d', obj.status))
        text = '#000' if obj.status == 'pending' else '#fff'
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600">{}</span>',
            color, text, label
        )
    status_badge.short_description = 'Status'

    @admin.action(description='✔ Accept selected applications')
    def accept_applications(self, request, queryset):
        updated = queryset.update(status='accepted')
        self.message_user(request, f'{updated} application(s) accepted.')

    @admin.action(description='✘ Reject selected applications')
    def reject_applications(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} application(s) rejected.')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'reviewee', 'mission', 'stars', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['reviewer__username', 'reviewee__username', 'mission__title']
    readonly_fields = ['created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'

    def stars(self, obj):
        filled = '★' * obj.rating
        empty = '☆' * (5 - obj.rating)
        return format_html('<span style="color:#ffc107;font-size:16px">{}</span><span style="color:#ccc;font-size:16px">{}</span>', filled, empty)
    stars.short_description = 'Rating'


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'target', 'reason', 'status_badge', 'created_at']
    list_filter = ['status', 'reason', 'created_at']
    search_fields = ['reporter__username', 'reported_mission__title', 'reported_user__username']
    readonly_fields = ['reporter', 'reported_mission', 'reported_user', 'reason', 'description', 'created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    actions = ['mark_reviewed', 'mark_dismissed']

    def target(self, obj):
        if obj.reported_mission:
            return format_html('<i class="bi bi-briefcase"></i> Mission: <strong>{}</strong>', obj.reported_mission.title)
        if obj.reported_user:
            return format_html('<i class="bi bi-person"></i> Profil: <strong>{}</strong>', obj.reported_user.username)
        return '—'
    target.short_description = 'Cible'

    def status_badge(self, obj):
        colors = {
            'pending':   ('#ffc107', '⏳ En attente'),
            'reviewed':  ('#198754', '✔ Traite'),
            'dismissed': ('#6c757d', '✘ Rejete'),
        }
        color, label = colors.get(obj.status, ('#6c757d', obj.status))
        text = '#000' if obj.status == 'pending' else '#fff'
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600">{}</span>',
            color, text, label
        )
    status_badge.short_description = 'Statut'

    @admin.action(description='✔ Marquer comme traite')
    def mark_reviewed(self, request, queryset):
        updated = queryset.update(status='reviewed')
        self.message_user(request, f'{updated} signalement(s) marque(s) comme traite(s).')

    @admin.action(description='✘ Rejeter les signalements')
    def mark_dismissed(self, request, queryset):
        updated = queryset.update(status='dismissed')
        self.message_user(request, f'{updated} signalement(s) rejete(s).')
