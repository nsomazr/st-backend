from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.emails import dispatch_booking_emails, send_status_update

from .models import Booking
from .serializers import (
    BookingCreateSerializer,
    BookingDetailSerializer,
    BookingListSerializer,
    BookingStatusUpdateSerializer,
)


class BookingCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        dispatch_booking_emails(booking.pk)

        return Response(
            BookingDetailSerializer(booking).data,
            status=status.HTTP_201_CREATED,
        )


class BookingListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingListSerializer

    def get_queryset(self):
        qs = Booking.objects.select_related('customer', 'service')
        params = self.request.query_params

        status_filter = params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)

        service_id = params.get('service')
        if service_id:
            qs = qs.filter(service_id=service_id)

        date_from = params.get('date_from')
        if date_from:
            qs = qs.filter(travel_date__gte=date_from)

        date_to = params.get('date_to')
        if date_to:
            qs = qs.filter(travel_date__lte=date_to)

        search = params.get('search')
        if search:
            qs = qs.filter(
                Q(booking_ref__icontains=search)
                | Q(customer__full_name__icontains=search)
                | Q(customer__email__icontains=search)
                | Q(destination__icontains=search)
            )

        return qs


class BookingDetailView(APIView):
    def get_permissions(self):
        return [AllowAny()]

    def get(self, request, ref):
        try:
            booking = Booking.objects.select_related('customer', 'service').get(booking_ref=ref)
        except Booking.DoesNotExist:
            return Response({'detail': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user and request.user.is_authenticated:
            return Response(BookingDetailSerializer(booking).data)

        return Response({
            'booking_ref': booking.booking_ref,
            'service_name': booking.service.name,
            'destination': booking.destination,
            'travel_date': booking.travel_date,
            'return_date': booking.return_date,
            'num_travelers': booking.num_travelers,
            'status': booking.status,
            'status_display': booking.get_status_display(),
        })


class BookingStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, ref):
        try:
            booking = Booking.objects.select_related('customer', 'service').get(booking_ref=ref)
        except Booking.DoesNotExist:
            return Response({'detail': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        old_status = booking.status
        serializer = BookingStatusUpdateSerializer(booking, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        if old_status != booking.status:
            send_status_update(booking)

        return Response(BookingDetailSerializer(booking).data)
