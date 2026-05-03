from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import User, StudentProfile, ClientProfile, PortfolioProject


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    extra = 0
    readonly_fields = ['average_rating', 'total_missions', 'verification_status']
    fields = [
        'photo', 'bio', 'school', 'field_of_study', 'skills',
        'github_url', 'linkedin_url', 'student_card',
        'verification_status', 'average_rating', 'total_missions',
    ]


class ClientProfileInline(admin.StackedInline):
    model = ClientProfile
    extra = 0
    readonly_fields = ['average_rating']
    fields = ['photo', 'client_type', 'company_name', 'bio', 'website', 'average_rating']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'full_name', 'role_badge', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    list_per_page = 25
    date_hierarchy = 'date_joined'
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('StuLance'), {'fields': ('role', 'phone')}),
    )

    def full_name(self, obj):
        return obj.get_full_name() or '—'
    full_name.short_description = 'Full Name'

    def role_badge(self, obj):
        colors = {
            'student': '#0d6efd',
            'client': '#198754',
            'admin': '#dc3545',
        }
        color = colors.get(obj.role, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600">{}</span>',
            color, obj.get_role_display() if hasattr(obj, 'get_role_display') else obj.role.title()
        )
    role_badge.short_description = 'Role'

    def get_inlines(self, request, obj=None):
        if obj:
            if obj.role == User.ROLE_STUDENT:
                return [StudentProfileInline]
            elif obj.role == User.ROLE_CLIENT:
                return [ClientProfileInline]
        return []


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'school', 'field_of_study', 'status_badge', 'average_rating', 'total_missions', 'card_preview']
    list_filter = ['verification_status', 'school']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'school', 'field_of_study']
    readonly_fields = ['average_rating', 'total_missions', 'card_preview']
    list_per_page = 20
    actions = ['verify_students', 'reject_students', 'set_pending']
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Academic', {'fields': ('school', 'field_of_study', 'student_card', 'card_preview', 'verification_status')}),
        ('Profile', {'fields': ('photo', 'bio', 'skills', 'github_url', 'linkedin_url')}),
        ('Stats', {'fields': ('average_rating', 'total_missions'), 'classes': ('collapse',)}),
    )

    def status_badge(self, obj):
        colors = {
            'verified': ('#198754', '✔ Verified'),
            'pending':  ('#ffc107', '⏳ Pending'),
            'rejected': ('#dc3545', '✘ Rejected'),
        }
        color, label = colors.get(obj.verification_status, ('#6c757d', obj.verification_status))
        text_color = '#000' if obj.verification_status == 'pending' else '#fff'
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600">{}</span>',
            color, text_color, label
        )
    status_badge.short_description = 'Status'

    def card_preview(self, obj):
        if obj.student_card:
            url = obj.student_card.url
            if url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                return format_html('<a href="{}" target="_blank"><img src="{}" style="height:60px;border-radius:6px;"></a>', url, url)
            return format_html('<a href="{}" target="_blank" class="btn btn-sm btn-outline-primary">View File</a>', url)
        return '—'
    card_preview.short_description = 'Student Card'

    @admin.action(description='✔ Verify selected student accounts')
    def verify_students(self, request, queryset):
        updated = queryset.update(verification_status='verified')
        self.message_user(request, f'{updated} student(s) verified successfully.')

    @admin.action(description='✘ Reject selected student accounts')
    def reject_students(self, request, queryset):
        updated = queryset.update(verification_status='rejected')
        self.message_user(request, f'{updated} student(s) rejected.')

    @admin.action(description='⏳ Set selected students back to pending')
    def set_pending(self, request, queryset):
        updated = queryset.update(verification_status='pending')
        self.message_user(request, f'{updated} student(s) set to pending.')


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'type_badge', 'company_name', 'average_rating', 'website_link']
    list_filter = ['client_type']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'company_name']
    readonly_fields = ['average_rating']
    list_per_page = 20

    def type_badge(self, obj):
        color = '#0d6efd' if obj.client_type == 'company' else '#6f42c1'
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600">{}</span>',
            color, obj.get_client_type_display()
        )
    type_badge.short_description = 'Type'

    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">🔗 Visit</a>', obj.website)
        return '—'
    website_link.short_description = 'Website'


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'url_link', 'created_at']
    search_fields = ['title', 'student__user__username']
    list_per_page = 20
    date_hierarchy = 'created_at'

    def url_link(self, obj):
        if obj.url:
            return format_html('<a href="{}" target="_blank">🔗 View</a>', obj.url)
        return '—'
    url_link.short_description = 'URL'
