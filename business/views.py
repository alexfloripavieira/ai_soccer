import json
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from business.forms import ClubForm, FinancialRecordForm, RevenueForm
from business.models import Club, FinancialRecord, Revenue
from performance.models import Athlete
from ml_models.revenue_forecaster import FORECAST_PERIODS, MINIMUM_SAMPLES, forecast_revenue


class ClubListView(LoginRequiredMixin, ListView):
    """
    Display list of clubs with search and filter capabilities.
    Supports search by name and country (GET parameter 'q').
    Supports filter by division (GET parameter 'division').
    """

    model = Club
    template_name = 'business/club_list.html'
    context_object_name = 'clubs'
    paginate_by = 20
    login_url = '/login/'

    def get_queryset(self):
        """
        Filter queryset based on search query and division filter.
        Search: matches name or country (case-insensitive).
        Filter: matches exact division value.
        """
        queryset = super().get_queryset()

        # Search functionality (9.2.6)
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(country__icontains=search_query)
            )

        # Division filter (9.2.7)
        division_filter = self.request.GET.get('division', '').strip()
        if division_filter:
            queryset = queryset.filter(division=division_filter)

        return queryset

    def get_context_data(self, **kwargs):
        """Add search query and division choices to context for template."""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_division'] = self.request.GET.get('division', '')
        context['division_choices'] = Club.DIVISION_CHOICES
        return context


class ClubCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new club instance.
    Automatically sets created_by to current user.
    """

    model = Club
    form_class = ClubForm
    template_name = 'business/club_form.html'
    success_url = reverse_lazy('business:club_list')
    login_url = '/login/'

    def form_valid(self, form):
        """Set created_by to current user before saving (9.2.9)."""
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add form title to context."""
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Criar Novo Clube'
        context['submit_text'] = 'Criar Clube'
        return context


class ClubDetailView(LoginRequiredMixin, DetailView):
    """
    Display detailed information about a specific club.
    """

    model = Club
    template_name = 'business/club_detail.html'
    context_object_name = 'club'
    login_url = '/login/'


class ClubUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update an existing club instance.
    """

    model = Club
    form_class = ClubForm
    template_name = 'business/club_form.html'
    login_url = '/login/'

    def get_success_url(self):
        """Redirect to club detail page after successful update."""
        return reverse_lazy('business:club_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """Add form title to context."""
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Clube'
        context['submit_text'] = 'Salvar Alterações'
        return context


class ClubDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a club instance with confirmation.
    """

    model = Club
    template_name = 'business/club_confirm_delete.html'
    context_object_name = 'club'
    success_url = reverse_lazy('business:club_list')
    login_url = '/login/'


class FinancialRecordListView(LoginRequiredMixin, ListView):
    """
    Display list of financial records with filters and totals calculation.
    Supports filter by club (GET parameter 'club_id').
    Supports filter by transaction type (GET parameter 'transaction_type').
    Supports filter by date range (GET parameters 'date_from' and 'date_to').
    """

    model = FinancialRecord
    template_name = 'business/financialrecord_list.html'
    context_object_name = 'financial_records'
    paginate_by = 20
    login_url = '/login/'

    def get_queryset(self):
        """
        Filter queryset based on club, transaction type, and date range.
        """
        queryset = super().get_queryset()

        # Club filter (10.2.5)
        club_id = self.request.GET.get('club_id', '').strip()
        if club_id:
            queryset = queryset.filter(club_id=club_id)

        # Transaction type filter (10.2.6)
        transaction_type = self.request.GET.get('transaction_type', '').strip()
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)

        # Date range filter (10.2.7)
        date_from = self.request.GET.get('date_from', '').strip()
        date_to = self.request.GET.get('date_to', '').strip()

        if date_from:
            queryset = queryset.filter(record_date__gte=date_from)

        if date_to:
            queryset = queryset.filter(record_date__lte=date_to)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add totals, filter parameters, and clubs to context.
        Calculate total revenue and total expenses (10.2.8).
        """
        context = super().get_context_data(**kwargs)
        zero = Decimal('0')

        # Get filtered queryset for totals calculation
        filtered_queryset = self.get_queryset()

        # Calculate totals (10.2.8)
        total_revenue = filtered_queryset.filter(transaction_type='RECEITA').aggregate(total=Sum('amount'))['total'] or zero

        total_expenses = filtered_queryset.filter(transaction_type='DESPESA').aggregate(total=Sum('amount'))['total'] or zero

        # Calculate net balance
        net_balance = total_revenue - total_expenses

        # Add totals to context
        context['total_revenue'] = total_revenue
        context['total_expenses'] = total_expenses
        context['net_balance'] = net_balance

        # Add filter parameters to context for template
        context['selected_club_id'] = self.request.GET.get('club_id', '')
        context['selected_transaction_type'] = self.request.GET.get('transaction_type', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')

        # Add clubs and transaction type choices for filters
        context['clubs'] = Club.objects.all().order_by('name')
        context['transaction_type_choices'] = FinancialRecord.TRANSACTION_TYPE_CHOICES

        return context


class FinancialRecordCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new financial record instance.
    Automatically sets created_by to current user.
    """

    model = FinancialRecord
    form_class = FinancialRecordForm
    template_name = 'business/financialrecord_form.html'
    success_url = reverse_lazy('business:financialrecord_list')
    login_url = '/login/'

    def form_valid(self, form):
        """Set created_by to current user before saving (10.2.9)."""
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Registro financeiro criado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add form title to context."""
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Criar Novo Registro Financeiro'
        context['submit_text'] = 'Criar Registro'
        return context


class FinancialRecordUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update an existing financial record instance.
    """

    model = FinancialRecord
    form_class = FinancialRecordForm
    template_name = 'business/financialrecord_form.html'
    success_url = reverse_lazy('business:financialrecord_list')
    login_url = '/login/'

    def form_valid(self, form):
        """Add success message after update (10.2.10)."""
        messages.success(self.request, 'Registro financeiro atualizado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add form title to context."""
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Registro Financeiro'
        context['submit_text'] = 'Salvar Alterações'
        return context


class FinancialRecordDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a financial record instance with confirmation.
    """

    model = FinancialRecord
    template_name = 'business/financialrecord_confirm_delete.html'
    context_object_name = 'financial_record'
    success_url = reverse_lazy('business:financialrecord_list')
    login_url = '/login/'

    def delete(self, request, *args, **kwargs):
        """Add success message after deletion (10.2.11)."""
        messages.success(self.request, 'Registro financeiro excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


class RevenueListView(LoginRequiredMixin, ListView):
    """
    Display list of monthly revenues with filters and totals calculation.
    Supports filter by club (GET parameter 'club_id').
    Supports filter by year (GET parameter 'year').
    Calculates totals for each revenue type and overall total.
    """

    model = Revenue
    template_name = 'business/revenue_list.html'
    context_object_name = 'revenues'
    paginate_by = 20
    login_url = '/login/'

    def get_queryset(self):
        """
        Filter queryset based on club and year.
        Ordered by -year, -month (10.4.4).
        """
        queryset = super().get_queryset()

        # Club filter (10.4.5)
        club_id = self.request.GET.get('club_id', '').strip()
        if club_id:
            queryset = queryset.filter(club_id=club_id)

        # Year filter (10.4.6)
        year = self.request.GET.get('year', '').strip()
        if year:
            queryset = queryset.filter(year=year)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add totals for each revenue type and overall total to context (10.4.7).
        Add filter parameters and clubs to context for template.
        """
        context = super().get_context_data(**kwargs)

        # Get filtered queryset for totals calculation
        filtered_queryset = self.get_queryset()

        zero = Decimal('0')

        # Calculate totals for each revenue type (10.4.7)
        total_ticketing = filtered_queryset.aggregate(total=Sum('ticketing'))['total'] or zero
        total_sponsorship = filtered_queryset.aggregate(total=Sum('sponsorship'))['total'] or zero
        total_broadcasting = filtered_queryset.aggregate(total=Sum('broadcasting'))['total'] or zero
        total_merchandising = filtered_queryset.aggregate(total=Sum('merchandising'))['total'] or zero

        # Calculate overall total revenue (10.4.8)
        total_revenue = (
            total_ticketing +
            total_sponsorship +
            total_broadcasting +
            total_merchandising
        )

        # Add totals to context
        context['total_ticketing'] = total_ticketing
        context['total_sponsorship'] = total_sponsorship
        context['total_broadcasting'] = total_broadcasting
        context['total_merchandising'] = total_merchandising
        context['total_revenue'] = total_revenue

        # Add filter parameters to context for template
        context['selected_club_id'] = self.request.GET.get('club_id', '')
        context['selected_year'] = self.request.GET.get('year', '')

        # Add clubs for filter dropdown
        context['clubs'] = Club.objects.all().order_by('name')

        # Add available years for filter dropdown
        context['available_years'] = Revenue.objects.values_list(
            'year', flat=True
        ).distinct().order_by('-year')

        return context


class RevenueCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new revenue instance.
    Automatically sets created_by to current user.
    Handles IntegrityError for unique_together constraint.
    """

    model = Revenue
    form_class = RevenueForm
    template_name = 'business/revenue_form.html'
    success_url = reverse_lazy('business:revenue_list')
    login_url = '/login/'

    def form_valid(self, form):
        """Set created_by to current user before saving (10.4.9)."""
        form.instance.created_by = self.request.user

        try:
            messages.success(self.request, 'Receita mensal criada com sucesso!')
            return super().form_valid(form)
        except Exception as e:
            # Handle IntegrityError for unique_together constraint (10.4.10)
            from django.db import IntegrityError
            if isinstance(e, IntegrityError):
                month_name = form.instance.get_month_display()
                form.add_error(
                    None,
                    f'Já existe um registro de receita para {form.instance.club.name} '
                    f'em {month_name}/{form.instance.year}. Cada clube pode ter apenas um registro por mês.'
                )
                return self.form_invalid(form)
            raise

    def get_context_data(self, **kwargs):
        """Add form title to context."""
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Criar Nova Receita Mensal'
        context['submit_text'] = 'Criar Receita'
        return context


class RevenueUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update an existing revenue instance.
    Club, year, and month fields are readonly to prevent changing unique_together key.
    """

    model = Revenue
    form_class = RevenueForm
    template_name = 'business/revenue_form.html'
    success_url = reverse_lazy('business:revenue_list')
    login_url = '/login/'

    def get_form(self, form_class=None):
        """
        Make club, year, and month readonly when updating (10.4.11).
        User can only update revenue values.
        """
        form = super().get_form(form_class)

        if self.object:
            # Disable club, year, month fields to prevent changing unique_together key
            form.fields['club'].disabled = True
            form.fields['year'].disabled = True
            form.fields['month'].disabled = True

            # Add help text to explain why fields are readonly
            form.fields['club'].help_text = 'O clube não pode ser alterado após a criação.'
            form.fields['year'].help_text = 'O ano não pode ser alterado após a criação.'
            form.fields['month'].help_text = 'O mês não pode ser alterado após a criação.'

        return form

    def form_valid(self, form):
        """Add success message after update (10.4.12)."""
        messages.success(self.request, 'Receita mensal atualizada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add form title to context."""
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Receita Mensal'
        context['submit_text'] = 'Salvar Alterações'
        return context


class RevenueDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a revenue instance with confirmation.
    """

    model = Revenue
    template_name = 'business/revenue_confirm_delete.html'
    context_object_name = 'revenue'
    success_url = reverse_lazy('business:revenue_list')
    login_url = '/login/'

    def delete(self, request, *args, **kwargs):
        """Add success message after deletion (10.4.13)."""
        messages.success(self.request, 'Receita mensal excluída com sucesso!')
        return super().delete(request, *args, **kwargs)


class FinancialDashboardView(LoginRequiredMixin, TemplateView):
    """
    Display comprehensive financial analytics dashboard.

    Provides financial overview across all clubs including:
    - Total revenues, expenses, and net balance (overall and per club)
    - Monthly revenue trends for last 12 months
    - Revenue breakdown by category from financial records
    - Recent financial transactions
    - Club count and individual club summaries

    Task 10.5: Financial Dashboard View
    """

    template_name = 'business/financial_dashboard.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        """
        Calculate comprehensive financial metrics and add to context (10.5.2 to 10.5.9).

        Context includes:
        - total_revenue: Overall revenue from all clubs
        - total_expenses: Overall expenses from all clubs
        - net_balance: Total revenue - total expenses
        - club_summaries: List of dicts with per-club financial data
        - monthly_revenues: Last 12 Revenue records ordered by year/month
        - revenue_by_category: Dict with category breakdown from FinancialRecords
        - recent_transactions: Last 10 FinancialRecord entries
        - clubs_count: Total number of clubs
        """
        context = super().get_context_data(**kwargs)
        zero = Decimal('0')

        # Calculate overall revenue (aggregate from FinancialRecord where RECEITA) (10.5.2)
        total_revenue = FinancialRecord.objects.filter(transaction_type='RECEITA').aggregate(total=Sum('amount'))['total'] or zero

        # Calculate overall expenses (aggregate from FinancialRecord where DESPESA) (10.5.3)
        total_expenses = FinancialRecord.objects.filter(transaction_type='DESPESA').aggregate(total=Sum('amount'))['total'] or zero

        # Calculate net balance (10.5.4)
        net_balance = total_revenue - total_expenses

        # Get all clubs and calculate per-club summaries (10.5.5)
        clubs = Club.objects.all().order_by('name')
        club_summaries = []

        for club in clubs:
            # Calculate revenues for this club
            club_revenues = FinancialRecord.objects.filter(
                club=club,
                transaction_type='RECEITA'
            ).aggregate(total=Sum('amount'))['total'] or zero

            # Calculate expenses for this club
            club_expenses = FinancialRecord.objects.filter(
                club=club,
                transaction_type='DESPESA'
            ).aggregate(total=Sum('amount'))['total'] or zero

            # Calculate balance for this club
            club_balance = club_revenues - club_expenses

            club_summaries.append({
                'club': club,
                'revenues': club_revenues,
                'expenses': club_expenses,
                'balance': club_balance
            })

        # Get last 12 monthly revenues ordered by year/month descending (10.5.6)
        monthly_revenues = Revenue.objects.all().order_by('-year', '-month')[:12]

        # Get revenue breakdown by category from FinancialRecord (10.5.7)
        revenue_by_category = {}
        for category_code, category_label in FinancialRecord.CATEGORY_CHOICES:
            category_total = FinancialRecord.objects.filter(
                transaction_type='RECEITA',
                category=category_code
            ).aggregate(total=Sum('amount'))['total'] or zero

            revenue_by_category[category_label] = category_total

        # Get expense breakdown by category from FinancialRecord (additional insight)
        expense_by_category = {}
        for category_code, category_label in FinancialRecord.CATEGORY_CHOICES:
            category_total = FinancialRecord.objects.filter(
                transaction_type='DESPESA',
                category=category_code
            ).aggregate(total=Sum('amount'))['total'] or zero

            expense_by_category[category_label] = category_total

        # Get recent transactions (last 10 FinancialRecord entries) (10.5.8)
        recent_transactions = FinancialRecord.objects.select_related(
            'club', 'created_by'
        ).order_by('-record_date', '-created_at')[:10]

        # Count total clubs (10.5.9)
        clubs_count = clubs.count()

        # Add all calculated data to context
        context['total_revenue'] = total_revenue
        context['total_expenses'] = total_expenses
        context['net_balance'] = net_balance
        context['club_summaries'] = club_summaries
        context['monthly_revenues'] = monthly_revenues
        context['revenue_by_category'] = revenue_by_category
        context['expense_by_category'] = expense_by_category
        context['recent_transactions'] = recent_transactions
        context['clubs_count'] = clubs_count

        # Integrate athlete market data from performance module (11.1.x)
        total_squad_value = Athlete.objects.aggregate(total=Sum('market_value'))['total'] or zero
        top_valued_athletes = Athlete.objects.filter(
            market_value__isnull=False
        ).select_related('created_by').order_by('-market_value')[:5]
        athletes_without_value = Athlete.objects.filter(market_value__isnull=True).count()

        context['total_squad_value'] = total_squad_value
        context['top_valued_athletes'] = top_valued_athletes
        context['athletes_without_value'] = athletes_without_value

        return context


class RevenueForecastView(LoginRequiredMixin, TemplateView):
    """Display revenue forecasts using the ML revenue forecaster."""

    template_name = 'business/revenue_forecast.html'
    login_url = reverse_lazy('accounts:login')

    CATEGORY_LABELS = {
        'ticketing': 'Bilheteria',
        'sponsorship': 'Patrocínio',
        'broadcasting': 'Direitos de transmissão',
        'merchandising': 'Merchandising',
    }

    def get_selected_club(self) -> Optional[Club]:
        """Return club instance selected via query parameter if available."""
        club_id = self.request.GET.get('club')
        if not club_id:
            return None
        try:
            return Club.objects.get(pk=int(club_id))
        except (Club.DoesNotExist, ValueError):
            return None

    def _build_distribution_entries(self, distribution: Dict[str, float]) -> List[Dict[str, float]]:
        """Convert category distribution dict into template-friendly entries."""
        entries: List[Dict[str, float]] = []
        for key, label in self.CATEGORY_LABELS.items():
            percentage = distribution.get(key, 0.0) * 100
            entries.append(
                {
                    'key': key,
                    'label': label,
                    'percentage': round(percentage, 2),
                }
            )
        return entries

    def _build_chart_points(self, points: List) -> List[Dict[str, object]]:
        """Return chart data combining historical and forecast points."""
        chart_points: List[Dict[str, object]] = []
        for point in points:
            chart_points.append(
                {
                    'label': point.label,
                    'value': round(point.total, 2),
                    'is_prediction': point.is_prediction,
                }
            )
        return chart_points

    def get_context_data(self, **kwargs):
        """Populate template context with forecast details."""
        context = super().get_context_data(**kwargs)
        selected_club = self.get_selected_club()
        forecast_result = forecast_revenue(club=selected_club, periods=FORECAST_PERIODS)

        historical_totals = [point.total for point in forecast_result.historical]
        latest_historical = historical_totals[-1] if historical_totals else 0.0
        predicted_totals = [point.total for point in forecast_result.predictions]
        next_prediction = predicted_totals[0] if predicted_totals else None

        growth_percentage = None
        if latest_historical and next_prediction is not None:
            growth_percentage = ((next_prediction - latest_historical) / latest_historical) * 100

        average_historical = (sum(historical_totals) / len(historical_totals)) if historical_totals else 0.0

        chart_points = self._build_chart_points(forecast_result.points)
        distribution_entries = self._build_distribution_entries(forecast_result.category_distribution)

        context.update(
            {
                'clubs': Club.objects.order_by('name'),
                'selected_club': selected_club,
                'forecast_result': forecast_result,
                'chart_points': chart_points,
                'chart_data_json': json.dumps(chart_points),
                'distribution_entries': distribution_entries,
                'latest_historical_total': latest_historical,
                'next_prediction_total': next_prediction,
                'growth_percentage': growth_percentage,
                'average_historical_total': average_historical,
                'minimum_samples': MINIMUM_SAMPLES,
                'forecast_periods': FORECAST_PERIODS,
                'has_predictions': bool(forecast_result.predictions),
                'has_historical': bool(forecast_result.historical),
            }
        )
        return context
