from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', views.home, name='home'),
    path('tos/', views.tos, name='tos'),
    path('help/', views.help_center, name='help'),
    path('contact/', views.contact, name='contact'),
    path('email-us/', views.email_us, name='email_us'),
    path('blog/', views.blog, name='blog'),
    path('accounts/', include('accounts.urls')),
    path('missions/', include('missions.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('messages/', include('messaging.urls')),
    path('notifications/', include('notifications.urls')),
    path('gigs/', include('gigs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
