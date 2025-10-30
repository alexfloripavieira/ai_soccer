from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View

from business.models import Club, FinancialRecord
from core.models import Notification
from performance.models import Athlete, InjuryRecord, TrainingLoad
from scouting.models import ScoutedPlayer, ScoutingReport


class NotificationListView(LoginRequiredMixin, ListView):
    """Display all notifications for the logged-in user."""

    model = Notification
    template_name = 'core/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20
    login_url = '/login/'

    def get_queryset(self):
        """Return notifications for the current user only."""
        return Notification.objects.filter(recipient=self.request.user).select_related(
            'sender',
            'content_type',
        )


class NotificationMarkAsReadView(LoginRequiredMixin, View):
    """Mark a notification as read."""

    login_url = '/login/'

    def post(self, request, pk):
        """Mark notification as read and redirect."""
        notification = get_object_or_404(
            Notification,
            pk=pk,
            recipient=request.user,
        )
        notification.mark_as_read()

        # Redirect to the notification link if available
        if notification.link:
            return redirect(notification.link)
        return redirect('notifications')


class NotificationMarkAllAsReadView(LoginRequiredMixin, View):
    """Mark all notifications as read."""

    login_url = '/login/'

    def post(self, request):
        """Mark all unread notifications as read."""
        Notification.objects.filter(
            recipient=request.user,
            is_read=False,
        ).update(is_read=True)
        return redirect('notifications')


class GlobalSearchView(LoginRequiredMixin, View):
    """
    Perform global search across multiple models.

    Searches in:
    - Athlete (name, nationality, position)
    - ScoutedPlayer (name, current_club, nationality)
    - Club (name, country)
    - InjuryRecord (athlete name, injury_type)
    - TrainingLoad (athlete name)
    - ScoutingReport (player name)
    - FinancialRecord (description, category)
    """

    login_url = '/login/'
    template_name = 'core/global_search.html'

    def get(self, request):
        """Handle GET request and perform search."""
        query = request.GET.get('q', '').strip()
        results = {
            'athletes': [],
            'scouted_players': [],
            'clubs': [],
            'injury_records': [],
            'training_loads': [],
            'scouting_reports': [],
            'financial_records': [],
        }
        total_results = 0

        if query:
            # Search in Athlete model (name, nationality, position)
            athletes = Athlete.objects.filter(
                Q(name__icontains=query) |
                Q(nationality__icontains=query) |
                Q(position__icontains=query)
            ).select_related('created_by')[:10]
            results['athletes'] = athletes
            total_results += athletes.count()

            # Search in ScoutedPlayer model (name, current_club, nationality)
            scouted_players = ScoutedPlayer.objects.filter(
                Q(name__icontains=query) |
                Q(current_club__icontains=query) |
                Q(nationality__icontains=query)
            ).select_related('created_by')[:10]
            results['scouted_players'] = scouted_players
            total_results += scouted_players.count()

            # Search in Club model (name, country)
            clubs = Club.objects.filter(
                Q(name__icontains=query) |
                Q(country__icontains=query)
            ).select_related('created_by')[:10]
            results['clubs'] = clubs
            total_results += clubs.count()

            # Search in InjuryRecord model (athlete name, injury_type)
            injury_records = InjuryRecord.objects.filter(
                Q(athlete__name__icontains=query) |
                Q(injury_type__icontains=query) |
                Q(body_part__icontains=query)
            ).select_related('athlete', 'created_by')[:10]
            results['injury_records'] = injury_records
            total_results += injury_records.count()

            # Search in TrainingLoad model (athlete name)
            training_loads = TrainingLoad.objects.filter(
                Q(athlete__name__icontains=query)
            ).select_related('athlete', 'created_by')[:10]
            results['training_loads'] = training_loads
            total_results += training_loads.count()

            # Search in ScoutingReport model (player name)
            scouting_reports = ScoutingReport.objects.filter(
                Q(player__name__icontains=query) |
                Q(match_or_event__icontains=query)
            ).select_related('player', 'created_by')[:10]
            results['scouting_reports'] = scouting_reports
            total_results += scouting_reports.count()

            # Search in FinancialRecord model (description, category)
            financial_records = FinancialRecord.objects.filter(
                Q(description__icontains=query) |
                Q(category__icontains=query) |
                Q(club__name__icontains=query)
            ).select_related('club', 'created_by')[:10]
            results['financial_records'] = financial_records
            total_results += financial_records.count()

        context = {
            'query': query,
            'results': results,
            'total_results': total_results,
        }

        return self.render_to_response(context)

    def render_to_response(self, context):
        """Render the template with the given context."""
        from django.shortcuts import render
        return render(self.request, self.template_name, context)
