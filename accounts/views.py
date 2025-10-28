"""Account views."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm


class HomeView(TemplateView):
    """Landing page view for AI Soccer."""

    template_name = 'home.html'


class SignUpView(SuccessMessageMixin, CreateView):
    """View responsible for user registration."""

    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    success_message = 'Conta criada com sucesso! Agora faça login para começar.'
