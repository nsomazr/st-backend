from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from bookings.models import Booking
from bookings.serializers import BookingListSerializer
from notifications.models import EmailLog
from notifications.serializers import EmailLogSerializer

from .models import Customer
from .serializers import AdminTokenObtainPairSerializer, CustomerSerializer


class AdminLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = AdminTokenObtainPairSerializer


class AdminDashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        bookings = Booking.objects.select_related('customer', 'service')

        by_service = (
            bookings.values('service__name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        upcoming = (
            bookings.filter(
                travel_date__gte=today,
                status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED],
            )
            .order_by('travel_date')[:5]
        )

        failed_emails = EmailLog.objects.filter(status=EmailLog.Status.FAILED).count()

        return Response({
            'total_bookings': bookings.count(),
            'pending': bookings.filter(status=Booking.Status.PENDING).count(),
            'confirmed': bookings.filter(status=Booking.Status.CONFIRMED).count(),
            'completed': bookings.filter(status=Booking.Status.COMPLETED).count(),
            'cancelled': bookings.filter(status=Booking.Status.CANCELLED).count(),
            'total_customers': Customer.objects.count(),
            'failed_emails': failed_emails,
            'bookings_by_service': [
                {'name': row['service__name'], 'count': row['count']}
                for row in by_service
            ],
            'recent_bookings': BookingListSerializer(bookings[:8], many=True).data,
            'upcoming_trips': BookingListSerializer(upcoming, many=True).data,
            'recent_failed_emails': EmailLogSerializer(
                EmailLog.objects.filter(status=EmailLog.Status.FAILED)[:5],
                many=True,
            ).data,
        })


class AdminCustomerListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    search_fields = ('full_name', 'email', 'phone', 'country')

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(full_name__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)
                | Q(country__icontains=search)
            )
        return qs


class AdminEmailLogListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmailLogSerializer
    queryset = EmailLog.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs
