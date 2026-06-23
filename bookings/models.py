import re

from django.db import models, transaction
from django.utils import timezone

from accounts.models import Customer
from services.models import Service

from .currency import fmt_budget_range


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'

    class BudgetRange(models.TextChoices):
        UNDER_500 = 'under_500', fmt_budget_range('under_500')
        RANGE_500_1500 = '500_1500', fmt_budget_range('500_1500')
        RANGE_1500_5000 = '1500_5000', fmt_budget_range('1500_5000')
        OVER_5000 = 'over_5000', fmt_budget_range('over_5000')

    booking_ref = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='bookings')
    travel_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    destination = models.CharField(max_length=200)
    num_travelers = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    budget_range = models.CharField(max_length=20, choices=BudgetRange.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.booking_ref or f'Booking #{self.pk}'

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            self.booking_ref = self._generate_booking_ref()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_booking_ref(cls):
        year = timezone.now().year
        prefix = f'ST-{year}-'

        with transaction.atomic():
            last_booking = (
                cls.objects.select_for_update()
                .filter(booking_ref__startswith=prefix)
                .order_by('-booking_ref')
                .first()
            )
            if last_booking:
                match = re.search(r'-(\d+)$', last_booking.booking_ref)
                next_num = int(match.group(1)) + 1 if match else 1
            else:
                next_num = 1

            return f'{prefix}{next_num:05d}'
