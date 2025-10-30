"""URL configuration for performance app."""

from django.urls import path

from performance.views import (
    AthleteCreateView,
    AthleteDeleteView,
    AthleteDetailView,
    AthleteListView,
    AthleteUpdateView,
    AthleteValuationView,
    ExportAthletesView,
    ExportTrainingLoadsView,
    InjuryRiskView,
    InjuryRecordCreateView,
    InjuryRecordDeleteView,
    InjuryRecordListView,
    InjuryRecordUpdateView,
    PerformanceDashboardView,
    TrainingLoadCreateView,
    TrainingLoadDeleteView,
    TrainingLoadListView,
    TrainingLoadUpdateView,
)

app_name = 'performance'

urlpatterns = [
    path('dashboard/', PerformanceDashboardView.as_view(), name='dashboard'),
    path('injury-risk/', InjuryRiskView.as_view(), name='injury_risk'),
    path('valuation/', AthleteValuationView.as_view(), name='athlete_valuation'),
    path('athletes/', AthleteListView.as_view(), name='athlete_list'),
    path('athletes/novo/', AthleteCreateView.as_view(), name='athlete_create'),
    path('athletes/exportar/', ExportAthletesView.as_view(), name='export_athletes'),
    path('athletes/<int:pk>/', AthleteDetailView.as_view(), name='athlete_detail'),
    path('athletes/<int:pk>/editar/', AthleteUpdateView.as_view(), name='athlete_update'),
    path('athletes/<int:pk>/excluir/', AthleteDeleteView.as_view(), name='athlete_delete'),
    path('training-loads/', TrainingLoadListView.as_view(), name='training_load_list'),
    path('training-loads/add/', TrainingLoadCreateView.as_view(), name='training_load_create'),
    path('training-loads/exportar/', ExportTrainingLoadsView.as_view(), name='export_training_loads'),
    path('training-loads/<int:pk>/editar/', TrainingLoadUpdateView.as_view(), name='training_load_update'),
    path('training-loads/<int:pk>/excluir/', TrainingLoadDeleteView.as_view(), name='training_load_delete'),
    path('injury-records/', InjuryRecordListView.as_view(), name='injury_record_list'),
    path('injury-records/novo/', InjuryRecordCreateView.as_view(), name='injury_record_create'),
    path('injury-records/<int:pk>/editar/', InjuryRecordUpdateView.as_view(), name='injury_record_update'),
    path('injury-records/<int:pk>/excluir/', InjuryRecordDeleteView.as_view(), name='injury_record_delete'),
]
