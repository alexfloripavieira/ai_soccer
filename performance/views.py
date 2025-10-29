from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from performance.forms import AthleteForm
from performance.models import Athlete


class AthleteListView(LoginRequiredMixin, ListView):
    """List all athletes with search and filter capabilities."""

    model = Athlete
    template_name = 'performance/athlete_list.html'
    context_object_name = 'athletes'
    paginate_by = 20
    login_url = '/login/'

    def get_queryset(self):
        """
        Return filtered queryset based on search query and position filter.

        Supports:
        - 'q' parameter: Search by athlete name (case-insensitive)
        - 'position' parameter: Filter by position code (GK, DF, MF, FW)
        """
        queryset = super().get_queryset()

        # Search by name
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        # Filter by position
        position_filter = self.request.GET.get('position', '').strip()
        if position_filter:
            queryset = queryset.filter(position=position_filter)

        return queryset

    def get_context_data(self, **kwargs):
        """Add position choices and current filters to context."""
        context = super().get_context_data(**kwargs)

        # Add position choices for filter dropdown
        context['position_choices'] = Athlete.POSITION_CHOICES

        # Add current filter values to preserve them in the template
        context['current_search'] = self.request.GET.get('q', '')
        context['current_position'] = self.request.GET.get('position', '')

        return context


class AthleteCreateView(LoginRequiredMixin, CreateView):
    """Create new athletes and bind them to the current user."""

    model = Athlete
    form_class = AthleteForm
    template_name = 'performance/athlete_form.html'
    success_url = reverse_lazy('performance:athlete_list')
    login_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class AthleteDetailView(LoginRequiredMixin, DetailView):
    """Display detailed information about a single athlete."""

    model = Athlete
    template_name = 'performance/athlete_detail.html'
    context_object_name = 'athlete'
    login_url = reverse_lazy('accounts:login')


class AthleteUpdateView(LoginRequiredMixin, UpdateView):
    """Allow editing of existing athlete records."""

    model = Athlete
    form_class = AthleteForm
    template_name = 'performance/athlete_form.html'
    login_url = reverse_lazy('accounts:login')

    def get_success_url(self):
        return reverse_lazy('performance:athlete_detail', args=[self.object.pk])


class AthleteDeleteView(LoginRequiredMixin, DeleteView):
    """Handle confirmation and removal of an athlete."""

    model = Athlete
    template_name = 'performance/athlete_confirm_delete.html'
    login_url = reverse_lazy('accounts:login')
    success_url = reverse_lazy('performance:athlete_list')
