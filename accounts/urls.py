from django.urls import path
from . import views

urlpatterns = [
    path('onboarding/', views.onboarding, name='onboarding'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/client/', views.register_client, name='register_client'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/student/', views.student_profile, name='student_profile'),
    path('profile/student/<int:pk>/', views.student_profile_detail, name='student_profile_detail'),
    path('profile/client/<int:pk>/', views.client_profile_detail, name='client_profile_detail'),
    path('profile/student/edit/', views.edit_student_profile, name='edit_student_profile'),
    path('profile/client/edit/', views.edit_client_profile, name='edit_client_profile'),
    path('portfolio/add/', views.add_portfolio_project, name='add_portfolio_project'),
    path('portfolio/delete/<int:pk>/', views.delete_portfolio_project, name='delete_portfolio_project'),
]
