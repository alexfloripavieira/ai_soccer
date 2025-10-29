from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from scouting.forms import ScoutedPlayerForm
from scouting.models import ScoutedPlayer


class ScoutedPlayerListView(LoginRequiredMixin, ListView):
    """Display list of scouted players with search and filters."""

    model = ScoutedPlayer
    template_name = 'scouting/scoutedplayer_list.html'
    context_object_name = 'players'
    paginate_by = 20
    login_url = reverse_lazy('accounts:login')

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related('created_by')
        )

        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        club_query = self.request.GET.get('club', '').strip()
        if club_query:
            queryset = queryset.filter(current_club__icontains=club_query)

        position_filter = self.request.GET.get('position', '').strip()
        if position_filter:
            queryset = queryset.filter(position=position_filter)

        status_filter = self.request.GET.get('status', '').strip()
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        order_by = self.request.GET.get('order', '').strip()
        allowed_ordering = {
            'market_value',
            '-market_value',
            'name',
            '-name',
            'birth_date',
            '-birth_date',
            'created_at',
            '-created_at',
        }
        if order_by in allowed_ordering:
            queryset = queryset.order_by(order_by)
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'position_choices': ScoutedPlayer.POSITION_CHOICES,
                'status_choices': ScoutedPlayer.STATUS_CHOICES,
                'order_choices': ScoutedPlayerForm.ORDER_BY_CHOICES,
                'current_search': self.request.GET.get('q', ''),
                'current_club': self.request.GET.get('club', ''),
                'current_position': self.request.GET.get('position', ''),
                'current_status': self.request.GET.get('status', ''),
                'current_order': self.request.GET.get('order', ''),
            }
        )
        return context


class ScoutedPlayerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create a new scouted player record."""

    model = ScoutedPlayer
    form_class = ScoutedPlayerForm
    template_name = 'scouting/scoutedplayer_form.html'
    success_url = reverse_lazy('scouting:player_list')
    success_message = 'Jogador observado cadastrado com sucesso.'
    login_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ScoutedPlayerDetailView(LoginRequiredMixin, DetailView):
    """Display details about a single scouted player."""

    model = ScoutedPlayer
    template_name = 'scouting/scoutedplayer_detail.html'
    context_object_name = 'player'
    login_url = reverse_lazy('accounts:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_photo'] = bool(self.object.photo)
        return context


class ScoutedPlayerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Edit an existing scouted player."""

    model = ScoutedPlayer
    form_class = ScoutedPlayerForm
    template_name = 'scouting/scoutedplayer_form.html'
    success_message = 'Jogador observado atualizado com sucesso.'
    login_url = reverse_lazy('accounts:login')

    def get_success_url(self):
        return reverse_lazy('scouting:player_detail', args=[self.object.pk])


class ScoutedPlayerDeleteView(LoginRequiredMixin, DeleteView):
    """Remove a scouted player after confirmation."""

    model = ScoutedPlayer
    template_name = 'scouting/scoutedplayer_confirm_delete.html'
    success_url = reverse_lazy('scouting:player_list')
    login_url = reverse_lazy('accounts:login')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Jogador observado removido com sucesso.')
        return super().delete(request, *args, **kwargs)
