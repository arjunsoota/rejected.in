from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path,include

urlpatterns = [
    path('',include('main.urls')),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('oauth/', include('social_django.urls', namespace="social")),
    path('admin/', admin.site.urls),
]
