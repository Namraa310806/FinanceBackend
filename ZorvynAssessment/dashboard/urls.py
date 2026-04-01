from django.urls import path

from dashboard.views import DashboardSummaryView

urlpatterns = [
    path('analytics/', DashboardSummaryView.as_view(), name='dashboard-analytics'),
    path('summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
]
