from django.urls import path

from .views import (
    AdminCustomerListView,
    AdminDashboardStatsView,
    AdminEmailLogListView,
    AdminLoginView,
)

urlpatterns = [
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('admin/dashboard/stats/', AdminDashboardStatsView.as_view(), name='admin-dashboard-stats'),
    path('admin/customers/', AdminCustomerListView.as_view(), name='admin-customers'),
    path('admin/emails/', AdminEmailLogListView.as_view(), name='admin-emails'),
]
