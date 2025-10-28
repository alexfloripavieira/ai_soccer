"""Account views."""

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView

from .forms import CustomAuthenticationForm, CustomUserCreationForm


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

    def get_success_url(self):
        return reverse_lazy('home')


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
