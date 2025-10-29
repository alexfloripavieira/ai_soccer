"""URL configuration for scouting app."""

from django.urls import path

from scouting.views import (
    ScoutedPlayerCreateView,
    ScoutedPlayerDeleteView,
    ScoutedPlayerDetailView,
    ScoutedPlayerListView,
    ScoutedPlayerUpdateView,
)

app_name = 'scouting'

urlpatterns = [
    path('jogadores/', ScoutedPlayerListView.as_view(), name='player_list'),
    path('jogadores/novo/', ScoutedPlayerCreateView.as_view(), name='player_create'),
    path('jogadores/<int:pk>/', ScoutedPlayerDetailView.as_view(), name='player_detail'),
    path('jogadores/<int:pk>/editar/', ScoutedPlayerUpdateView.as_view(), name='player_update'),
    path('jogadores/<int:pk>/excluir/', ScoutedPlayerDeleteView.as_view(), name='player_delete'),
]
