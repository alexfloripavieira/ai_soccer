"""Account views."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView

from .forms import CustomAuthenticationForm, CustomUserCreationForm, ProfileUpdateForm


class HomeView(TemplateView):
    """Landing page view for AI Soccer."""

    template_name = 'home.html'


class SignUpView(SuccessMessageMixin, CreateView):
    """View responsible for user registration."""

    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    success_message = 'Conta criada com sucesso! Agora faça login para começar.'


class LoginView(SuccessMessageMixin, AuthLoginView):
    """Login view accepting e-mail as credential."""

    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True
    success_message = 'Bem-vindo de volta ao AI Soccer!'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class LogoutView(AuthLogoutView):
    """Ends the session and redirects to landing page."""

    next_page = reverse_lazy('home')
    http_method_names = ['get', 'post', 'head', 'options']

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, 'Você saiu do AI Soccer com segurança. Até breve!')
        return response

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    """Protected dashboard view accessible only to authenticated users."""

    template_name = 'dashboard/home.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        """Add user-specific data to the dashboard context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    """Display current user profile summary."""

    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        full_name = ' '.join(part for part in [user.first_name, user.last_name] if part)
        context['profile_full_name'] = full_name or user.email
        return context


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Allow users to update basic profile information."""

    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_message = 'Perfil atualizado com sucesso!'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('accounts:profile')
