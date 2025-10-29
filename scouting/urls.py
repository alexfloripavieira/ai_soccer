"""URL configuration for scouting app."""

from django.urls import path

from scouting.views import (
    ScoutedPlayerCreateView,
    ScoutedPlayerDeleteView,
    ScoutedPlayerDetailView,
    ScoutedPlayerListView,
    ScoutedPlayerUpdateView,
    ScoutingDashboardView,
    ScoutingReportCreateView,
    ScoutingReportDeleteView,
    ScoutingReportDetailView,
    ScoutingReportListView,
    ScoutingReportUpdateView,
)

app_name = 'scouting'

urlpatterns = [
    path('dashboard/', ScoutingDashboardView.as_view(), name='dashboard'),
    path('jogadores/', ScoutedPlayerListView.as_view(), name='player_list'),
    path('jogadores/novo/', ScoutedPlayerCreateView.as_view(), name='player_create'),
    path('jogadores/<int:pk>/', ScoutedPlayerDetailView.as_view(), name='player_detail'),
    path('jogadores/<int:pk>/editar/', ScoutedPlayerUpdateView.as_view(), name='player_update'),
    path('jogadores/<int:pk>/excluir/', ScoutedPlayerDeleteView.as_view(), name='player_delete'),
    path('relatorios/', ScoutingReportListView.as_view(), name='report_list'),
    path('relatorios/novo/', ScoutingReportCreateView.as_view(), name='report_create'),
    path('relatorios/<int:pk>/', ScoutingReportDetailView.as_view(), name='report_detail'),
    path('relatorios/<int:pk>/editar/', ScoutingReportUpdateView.as_view(), name='report_update'),
    path('relatorios/<int:pk>/excluir/', ScoutingReportDeleteView.as_view(), name='report_delete'),
]
