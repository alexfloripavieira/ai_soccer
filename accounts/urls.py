"""URLs for accounts app."""

from django.urls import path

from .views import (
    DashboardView,
    LoginView,
    LogoutView,
    ProfileUpdateView,
    ProfileView,
    SignUpView,
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/editar/', ProfileUpdateView.as_view(), name='profile-edit'),
]
