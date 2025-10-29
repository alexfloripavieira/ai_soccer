"""URL configuration for performance app."""

from django.urls import path

from performance.views import (
    AthleteCreateView,
    AthleteDeleteView,
    AthleteDetailView,
    AthleteListView,
    AthleteUpdateView,
    TrainingLoadCreateView,
    TrainingLoadDeleteView,
    TrainingLoadListView,
    TrainingLoadUpdateView,
)

app_name = 'performance'

urlpatterns = [
    path('athletes/', AthleteListView.as_view(), name='athlete_list'),
    path('athletes/novo/', AthleteCreateView.as_view(), name='athlete_create'),
    path('athletes/<int:pk>/', AthleteDetailView.as_view(), name='athlete_detail'),
    path('athletes/<int:pk>/editar/', AthleteUpdateView.as_view(), name='athlete_update'),
    path('athletes/<int:pk>/excluir/', AthleteDeleteView.as_view(), name='athlete_delete'),
    path('training-loads/', TrainingLoadListView.as_view(), name='training_load_list'),
    path('training-loads/add/', TrainingLoadCreateView.as_view(), name='training_load_create'),
    path('training-loads/<int:pk>/editar/', TrainingLoadUpdateView.as_view(), name='training_load_update'),
    path('training-loads/<int:pk>/excluir/', TrainingLoadDeleteView.as_view(), name='training_load_delete'),
]
