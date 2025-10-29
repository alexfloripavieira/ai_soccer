from django.urls import path

from business.views import (
    ClubCreateView,
    ClubDeleteView,
    ClubDetailView,
    ClubListView,
    ClubUpdateView,
    FinancialDashboardView,
    FinancialRecordCreateView,
    FinancialRecordDeleteView,
    FinancialRecordListView,
    FinancialRecordUpdateView,
    RevenueCreateView,
    RevenueDeleteView,
    RevenueForecastView,
    RevenueListView,
    RevenueUpdateView,
)

app_name = 'business'

urlpatterns = [
    # Dashboard (10.5.10)
    path('dashboard/', FinancialDashboardView.as_view(), name='financial_dashboard'),
    # Club CRUD URLs
    path('clubs/', ClubListView.as_view(), name='club_list'),
    path('clubs/create/', ClubCreateView.as_view(), name='club_create'),
    path('clubs/<int:pk>/', ClubDetailView.as_view(), name='club_detail'),
    path('clubs/<int:pk>/edit/', ClubUpdateView.as_view(), name='club_update'),
    path('clubs/<int:pk>/delete/', ClubDeleteView.as_view(), name='club_delete'),
    # FinancialRecord CRUD URLs (10.2.13, 10.2.14)
    path('financial-records/', FinancialRecordListView.as_view(), name='financialrecord_list'),
    path('financial-records/add/', FinancialRecordCreateView.as_view(), name='financialrecord_create'),
    path('financial-records/<int:pk>/edit/', FinancialRecordUpdateView.as_view(), name='financialrecord_update'),
    path('financial-records/<int:pk>/delete/', FinancialRecordDeleteView.as_view(), name='financialrecord_delete'),
    # Revenue CRUD URLs (10.4.13, 10.4.14)
    path('revenues/', RevenueListView.as_view(), name='revenue_list'),
    path('revenues/add/', RevenueCreateView.as_view(), name='revenue_create'),
    path('revenues/<int:pk>/edit/', RevenueUpdateView.as_view(), name='revenue_update'),
    path('revenues/<int:pk>/delete/', RevenueDeleteView.as_view(), name='revenue_delete'),
    # Revenue forecast (13.5.x)
    path('forecast/', RevenueForecastView.as_view(), name='revenue_forecast'),
]
