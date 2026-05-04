from django.urls import path
from . import views

urlpatterns = [
    path('', views.mission_list, name='mission_list'),
    path('create/', views.mission_create, name='mission_create'),
    path('<int:pk>/', views.mission_detail, name='mission_detail'),
    path('<int:pk>/edit/', views.mission_edit, name='mission_edit'),
    path('<int:pk>/delete/', views.mission_delete, name='mission_delete'),
    path('<int:pk>/apply/', views.apply_mission, name='apply_mission'),
    path('<int:pk>/applications/', views.mission_applications, name='mission_applications'),
    path('application/<int:pk>/accept/', views.accept_application, name='accept_application'),
    path('application/<int:pk>/reject/', views.reject_application, name='reject_application'),
    path('<int:pk>/complete/', views.complete_mission, name='complete_mission'),
    path('<int:pk>/review/', views.leave_review, name='leave_review'),
    path('<int:pk>/report/', views.report_mission, name='report_mission'),
    path('report-user/<int:pk>/', views.report_user, name='report_user'),
]
