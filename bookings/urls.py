from django.urls import path

from .views import (
    BookingCreateView,
    BookingDetailView,
    BookingListView,
    BookingStatusUpdateView,
)

urlpatterns = [
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/<str:ref>/', BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/<str:ref>/status/', BookingStatusUpdateView.as_view(), name='booking-status-update'),
]
