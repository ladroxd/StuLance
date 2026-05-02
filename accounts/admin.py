from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, ClientProfile, PortfolioProject


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    extra = 0


class ClientProfileInline(admin.StackedInline):
    model = ClientProfile
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role', {'fields': ('role', 'phone')}),
    )

    def get_inlines(self, request, obj=None):
        if obj:
            if obj.role == User.ROLE_STUDENT:
                return [StudentProfileInline]
            elif obj.role == User.ROLE_CLIENT:
                return [ClientProfileInline]
        return []


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'school', 'verification_status', 'average_rating', 'total_missions']
    list_filter = ['verification_status']
    actions = ['verify_students', 'reject_students']

    @admin.action(description='Valider les comptes etudiants selectionnes')
    def verify_students(self, request, queryset):
        queryset.update(verification_status='verified')

    @admin.action(description='Rejeter les comptes etudiants selectionnes')
    def reject_students(self, request, queryset):
        queryset.update(verification_status='rejected')


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'client_type', 'company_name', 'average_rating']


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'created_at']
