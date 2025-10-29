from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Max, Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from performance.forms import AthleteForm, TrainingLoadForm
from performance.models import Athlete, TrainingLoad


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_training_loads = list(
            self.object.training_loads.select_related('athlete')
            .order_by('-training_date')[:10]
        )
        aggregates = self.object.training_loads.aggregate(
            avg_duration=Avg('duration_minutes'),
            total_distance=Sum('distance_km'),
        )
        intensity_map = {
            TrainingLoad.INTENSITY_LOW: 1,
            TrainingLoad.INTENSITY_MEDIUM: 2,
            TrainingLoad.INTENSITY_HIGH: 3,
            TrainingLoad.INTENSITY_VERY_HIGH: 4,
        }

        context.update(
            {
                'latest_training_loads': latest_training_loads,
                'has_training_loads': bool(latest_training_loads),
                'training_load_average_duration': (
                    float(aggregates['avg_duration']) if aggregates['avg_duration'] else 0.0
                ),
                'training_load_total_distance': (
                    float(aggregates['total_distance']) if aggregates['total_distance'] else 0.0
                ),
                'training_load_count': self.object.training_loads.count(),
                'training_load_list_url': reverse_lazy('performance:training_load_list'),
                'training_load_chart_data': [
                    {
                        'date': load.training_date.strftime('%d/%m'),
                        'intensity': intensity_map.get(load.intensity_level, 0),
                        'label': load.get_intensity_level_display(),
                    }
                    for load in latest_training_loads
                ],
            }
        )
        return context


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


class TrainingLoadListView(LoginRequiredMixin, ListView):
    """List training loads with filters for athlete and period."""

    model = TrainingLoad
    template_name = 'performance/training_load_list.html'
    context_object_name = 'training_loads'
    paginate_by = 15
    login_url = reverse_lazy('accounts:login')

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related('athlete', 'created_by')
            .order_by('-training_date', '-created_at')
        )
        athlete_id = self.request.GET.get('athlete')
        if athlete_id:
            queryset = queryset.filter(athlete_id=athlete_id)

        period = self.request.GET.get('period')
        if period:
            today = date.today()
            periods = {
                'last_7_days': today - timedelta(days=7),
                'last_30_days': today - timedelta(days=30),
                'last_90_days': today - timedelta(days=90),
            }
            start_date = periods.get(period)
            if start_date:
                queryset = queryset.filter(training_date__gte=start_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['athletes'] = Athlete.objects.order_by('name')
        context['selected_athlete'] = self.request.GET.get('athlete', '')
        context['selected_period'] = self.request.GET.get('period', '')
        context['period_options'] = TrainingLoadForm.PERIOD_CHOICES
        context['params'] = self.request.GET.copy()
        context['params'].pop('page', None)
        context['total_records'] = self.get_queryset().count()
        aggregates = self.get_queryset().aggregate(
            avg_duration=Avg('duration_minutes'),
            latest_training_date=Max('training_date'),
        )
        context['average_duration'] = (
            float(aggregates['avg_duration']) if aggregates['avg_duration'] else 0.0
        )
        context['latest_training_date'] = aggregates['latest_training_date']
        return context


class TrainingLoadCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create a new training load entry."""

    model = TrainingLoad
    form_class = TrainingLoadForm
    template_name = 'performance/training_load_form.html'
    login_url = reverse_lazy('accounts:login')
    success_url = reverse_lazy('performance:training_load_list')
    success_message = 'Carga de treino registrada com sucesso.'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['athlete'].queryset = Athlete.objects.order_by('name')
        return form


class TrainingLoadUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update an existing training load."""

    model = TrainingLoad
    form_class = TrainingLoadForm
    template_name = 'performance/training_load_form.html'
    login_url = reverse_lazy('accounts:login')
    success_url = reverse_lazy('performance:training_load_list')
    success_message = 'Carga de treino atualizada com sucesso.'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['athlete'].queryset = Athlete.objects.order_by('name')
        return form


class TrainingLoadDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a training load after confirmation."""

    model = TrainingLoad
    template_name = 'performance/training_load_confirm_delete.html'
    login_url = reverse_lazy('accounts:login')
    success_url = reverse_lazy('performance:training_load_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Carga de treino removida com sucesso.')
        return super().delete(request, *args, **kwargs)
