from django.shortcuts import render
from missions.models import Mission, Category

def home(request):
    missions = Mission.objects.filter(status='open').order_by('-created_at')[:6]
    categories = Category.objects.all()
    return render(request, 'home.html', {'missions': missions, 'categories': categories})
