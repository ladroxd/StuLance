from django.contrib import admin
from django.utils.html import format_html
from .models import Gig


@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'category', 'rate_display', 'delivery_days', 'extras_count', 'approval_badge', 'status_badge', 'created_at']
    list_filter = ['status', 'is_active', 'category', 'created_at']
    search_fields = ['title', 'description', 'student__username']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    actions = ['approve_gigs', 'reject_gigs', 'activate_gigs', 'deactivate_gigs']

    def rate_display(self, obj):
        return format_html('<strong style="color:#198754">{} MAD</strong>', obj.base_rate)
    rate_display.short_description = 'Tarif de base'

    def extras_count(self, obj):
        count = len(obj.extras) if obj.extras else 0
        return format_html('<span style="font-weight:600">{}</span>', count)
    extras_count.short_description = 'Extras'

    def approval_badge(self, obj):
        colors = {
            'pending':  ('#ffc107', '#000', '⏳ En attente'),
            'approved': ('#198754', '#fff', '✔ Approuvé'),
            'rejected': ('#dc3545', '#fff', '✘ Rejeté'),
        }
        bg, fg, label = colors.get(obj.status, ('#6c757d', '#fff', obj.status))
        return format_html('<span style="background:{};color:{};padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600">{}</span>', bg, fg, label)
    approval_badge.short_description = 'Approbation'

    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background:#198754;color:#fff;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600">Actif</span>')
        return format_html('<span style="background:#dc3545;color:#fff;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600">Inactif</span>')
    status_badge.short_description = 'Visibilité'

    @admin.action(description='✔ Approuver les services sélectionnés')
    def approve_gigs(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} service(s) approuvé(s).')

    @admin.action(description='✘ Rejeter les services sélectionnés')
    def reject_gigs(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} service(s) rejeté(s).')

    @admin.action(description='✔ Activer les services sélectionnés')
    def activate_gigs(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} service(s) activé(s).')

    @admin.action(description='✘ Désactiver les services sélectionnés')
    def deactivate_gigs(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} service(s) désactivé(s).')
