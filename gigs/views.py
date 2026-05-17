import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext as _
from missions.models import Category
from missions.utils import get_all_categories
from .models import Gig


def gig_list(request):
    qs = Gig.objects.filter(is_active=True, status='approved').select_related('student', 'student__student_profile', 'category')
    q = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    rate_max = request.GET.get('rate_max', '')

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(skills__icontains=q))
    if category_id:
        qs = qs.filter(category_id=category_id)
    if rate_max:
        qs = qs.filter(base_rate__lte=rate_max)

    categories = get_all_categories()
    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'gigs/list.html', {
        'gigs': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'q': q,
    })


def gig_detail(request, pk):
    gig = get_object_or_404(Gig, pk=pk)
    # Owner can always preview; others only see approved gigs
    if gig.student != request.user and gig.status != 'approved':
        from django.http import Http404
        raise Http404
    return render(request, 'gigs/detail.html', {'gig': gig})


@login_required
def gig_create(request):
    if not request.user.is_student():
        messages.error(request, _('Only students can post services.'))
        return redirect('gig_list')
    if request.method == 'POST':
        return _save_gig(request, gig=None)
    profile = request.user.student_profile
    categories = get_all_categories()
    return render(request, 'gigs/form.html', {
        'action': _('Publish'),
        'categories': categories,
        'default_rate': profile.hourly_rate or '',
        'gig': None,
    })


@login_required
def gig_edit(request, pk):
    gig = get_object_or_404(Gig, pk=pk, student=request.user)
    if request.method == 'POST':
        return _save_gig(request, gig=gig)
    categories = get_all_categories()
    return render(request, 'gigs/form.html', {
        'action': _('Edit'),
        'categories': categories,
        'default_rate': gig.base_rate,
        'gig': gig,
    })


@login_required
def gig_delete(request, pk):
    gig = get_object_or_404(Gig, pk=pk, student=request.user)
    if request.method == 'POST':
        gig.delete()
        messages.success(request, _('Service deleted.'))
        return redirect('dashboard')
    return render(request, 'gigs/confirm_delete.html', {'gig': gig})


@login_required
def my_gigs(request):
    if not request.user.is_student():
        return redirect('dashboard')
    gigs = Gig.objects.filter(student=request.user)
    return render(request, 'gigs/my_gigs.html', {'gigs': gigs})


def _save_gig(request, gig):
    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    category_id = request.POST.get('category')
    skills = request.POST.get('skills', '').strip()
    base_rate = request.POST.get('base_rate', '').strip()
    delivery_days = request.POST.get('delivery_days', '').strip()

    # Parse extras from POST
    extra_labels = request.POST.getlist('extra_label')
    extra_descs = request.POST.getlist('extra_description')
    extra_prices = request.POST.getlist('extra_price')
    extras = []
    for label, desc, price in zip(extra_labels, extra_descs, extra_prices):
        label = label.strip()
        price = price.strip()
        if label and price:
            try:
                extras.append({'label': label, 'description': desc.strip(), 'price': float(price)})
            except ValueError:
                pass

    errors = []
    if not title:
        errors.append(_('Title is required.'))
    if not description:
        errors.append(_('Description is required.'))
    if not base_rate:
        errors.append(_('Base rate is required.'))
    if not delivery_days:
        errors.append(_('Delivery time is required.'))

    categories = get_all_categories()
    if errors:
        for e in errors:
            messages.error(request, e)
        return render(request, 'gigs/form.html', {
            'action': _('Publish') if gig is None else _('Edit'),
            'categories': categories,
            'default_rate': base_rate,
            'gig': gig,
        })

    if gig is None:
        gig = Gig(student=request.user)

    is_edit = gig.pk is not None
    gig.title = title
    gig.description = description
    gig.category_id = category_id or None
    gig.skills = skills
    gig.base_rate = base_rate
    gig.delivery_days = delivery_days
    gig.extras = extras
    if is_edit:
        gig.status = Gig.STATUS_PENDING  # re-submit for approval on every edit
    gig.save()

    messages.success(request, _('Service saved.'))
    return redirect('gig_detail', pk=gig.pk)
