"""Account views."""

from datetime import timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView

from auditlog.models import LogEntry

from business.models import Club, FinancialRecord
from performance.models import Athlete, InjuryRecord, TrainingLoad
from scouting.models import ScoutedPlayer, ScoutingReport

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
        user = self.request.user
        context['user'] = user

        today = timezone.localdate()
        last_seven_days = today - timedelta(days=7)

        total_athletes = Athlete.objects.count()
        total_reports = ScoutingReport.objects.count()
        total_scouted = ScoutedPlayer.objects.count()
        total_clubs = Club.objects.count()
        total_financials = FinancialRecord.objects.count()
        active_sessions = TrainingLoad.objects.filter(training_date__gte=last_seven_days).count()
        total_squad_value = (
            Athlete.objects.aggregate(total=Sum('market_value')).get('total')
            or Decimal('0')
        )
        monitoring_players = ScoutedPlayer.objects.exclude(status=ScoutedPlayer.STATUS_HIRED).count()

        recent_athletes = (
            Athlete.objects.select_related('created_by')
            .order_by('-created_at')[:5]
        )
        recent_injuries = (
            InjuryRecord.objects.select_related('athlete')
            .order_by('-injury_date', '-created_at')[:5]
        )
        recent_reports = (
            ScoutingReport.objects.select_related('player')
            .order_by('-report_date', '-created_at')[:5]
        )
        recent_financials = (
            FinancialRecord.objects.select_related('club')
            .order_by('-record_date', '-created_at')[:5]
        )

        context.update(
            {
                'total_athletes': total_athletes,
                'total_reports': total_reports,
                'total_financials': total_financials,
                'active_sessions': active_sessions,
                'total_squad_value': total_squad_value,
                'monitoring_players': monitoring_players,
                'total_scouted': total_scouted,
                'total_clubs': total_clubs,
                'recent_athletes': recent_athletes,
                'recent_injuries': recent_injuries,
                'recent_reports': recent_reports,
                'recent_financials': recent_financials,
            }
        )
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


class AuditLogListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    View to list audit logs from django-auditlog.

    Restricted to staff/superuser only. Provides filtering by:
    - Action type (create, update, delete)
    - Model (content_type)
    - User (actor)
    - Date range
    - Object ID search
    """

    model = LogEntry
    template_name = 'accounts/audit_log_list.html'
    context_object_name = 'logs'
    paginate_by = 20
    login_url = '/login/'

    def test_func(self):
        """Only allow staff or superuser access."""
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        """
        Get filtered queryset based on query parameters.

        Supports filtering by:
        - action: create (0), update (1), delete (2)
        - model: ContentType ID
        - user: User ID
        - date_from: Start date (YYYY-MM-DD)
        - date_to: End date (YYYY-MM-DD)
        - object_id: Search by object ID
        """
        queryset = LogEntry.objects.select_related(
            'actor', 'content_type'
        ).order_by('-timestamp')

        # Filter by action type
        action = self.request.GET.get('action')
        if action:
            queryset = queryset.filter(action=action)

        # Filter by model (content_type)
        model = self.request.GET.get('model')
        if model:
            queryset = queryset.filter(content_type_id=model)

        # Filter by user (actor)
        user = self.request.GET.get('user')
        if user:
            queryset = queryset.filter(actor_id=user)

        # Filter by date range
        date_from = self.request.GET.get('date_from')
        if date_from:
            queryset = queryset.filter(timestamp__date__gte=date_from)

        date_to = self.request.GET.get('date_to')
        if date_to:
            queryset = queryset.filter(timestamp__date__lte=date_to)

        # Search by object ID
        object_id = self.request.GET.get('object_id')
        if object_id:
            queryset = queryset.filter(object_id=object_id)

        return queryset

    def get_context_data(self, **kwargs):
        """Add filter options and current filter values to context."""
        context = super().get_context_data(**kwargs)

        # Add action choices for filter dropdown
        context['action_choices'] = [
            ('0', 'Criar'),
            ('1', 'Atualizar'),
            ('2', 'Deletar'),
        ]

        # Get all content types that have audit logs
        context['model_choices'] = ContentType.objects.filter(
            logentry__isnull=False
        ).distinct().order_by('model')

        # Get all users who have performed actions
        from django.contrib.auth import get_user_model
        User = get_user_model()
        context['user_choices'] = User.objects.filter(
            id__in=LogEntry.objects.values_list('actor_id', flat=True).distinct()
        ).order_by('email')

        # Preserve current filter values
        context['current_action'] = self.request.GET.get('action', '')
        context['current_model'] = self.request.GET.get('model', '')
        context['current_user'] = self.request.GET.get('user', '')
        context['current_date_from'] = self.request.GET.get('date_from', '')
        context['current_date_to'] = self.request.GET.get('date_to', '')
        context['current_object_id'] = self.request.GET.get('object_id', '')

        return context
