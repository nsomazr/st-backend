from rest_framework import serializers

from accounts.models import Customer
from accounts.serializers import CustomerSerializer
from services.serializers import ServiceSerializer

from .models import Booking


class BookingCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=30)
    country = serializers.CharField(max_length=100)
    service_id = serializers.IntegerField()
    travel_date = serializers.DateField()
    return_date = serializers.DateField(required=False, allow_null=True)
    destination = serializers.CharField(max_length=200)
    num_travelers = serializers.IntegerField(min_value=1)
    special_requests = serializers.CharField(required=False, allow_blank=True, default='')
    budget_range = serializers.ChoiceField(choices=Booking.BudgetRange.choices)

    def validate_service_id(self, value):
        from services.models import Service
        if not Service.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError('Invalid or inactive service.')
        return value

    def validate(self, data):
        return_date = data.get('return_date')
        travel_date = data.get('travel_date')
        if return_date and return_date < travel_date:
            raise serializers.ValidationError({'return_date': 'Return date must be after travel date.'})
        return data

    def create(self, validated_data):
        customer, _ = Customer.objects.update_or_create(
            email=validated_data['email'],
            defaults={
                'full_name': validated_data['full_name'],
                'phone': validated_data['phone'],
                'country': validated_data['country'],
            },
        )
        booking = Booking.objects.create(
            customer=customer,
            service_id=validated_data['service_id'],
            travel_date=validated_data['travel_date'],
            return_date=validated_data.get('return_date'),
            destination=validated_data['destination'],
            num_travelers=validated_data['num_travelers'],
            special_requests=validated_data.get('special_requests', ''),
            budget_range=validated_data['budget_range'],
        )
        return booking


class BookingListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    customer_email = serializers.CharField(source='customer.email', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    budget_range_display = serializers.CharField(source='get_budget_range_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id', 'booking_ref', 'customer_name', 'customer_email', 'customer_phone',
            'service_name', 'destination', 'travel_date', 'return_date',
            'num_travelers', 'special_requests', 'status', 'status_display',
            'budget_range', 'budget_range_display', 'created_at', 'updated_at',
        )


class BookingDetailSerializer(BookingListSerializer):
    customer = CustomerSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta(BookingListSerializer.Meta):
        fields = BookingListSerializer.Meta.fields + ('customer', 'service',)


class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('status',)
