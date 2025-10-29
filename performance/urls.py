"""URL configuration for performance app."""

from django.urls import path

from performance.views import (
    AthleteCreateView,
    AthleteDetailView,
    AthleteListView,
    AthleteDeleteView,
    AthleteUpdateView,
)

app_name = 'performance'

urlpatterns = [
    path('athletes/', AthleteListView.as_view(), name='athlete_list'),
    path('athletes/novo/', AthleteCreateView.as_view(), name='athlete_create'),
    path('athletes/<int:pk>/', AthleteDetailView.as_view(), name='athlete_detail'),
    path('athletes/<int:pk>/editar/', AthleteUpdateView.as_view(), name='athlete_update'),
    path('athletes/<int:pk>/excluir/', AthleteDeleteView.as_view(), name='athlete_delete'),
]
