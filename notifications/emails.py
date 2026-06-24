import logging
import threading

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import close_old_connections
from django.template.loader import render_to_string
from django.utils import timezone

from bookings.currency import fmt_budget_range

from .models import EmailLog

logger = logging.getLogger(__name__)


def _send_html_email(recipient, subject, template_name, context):
    context = {
        **context,
        'frontend_url': settings.FRONTEND_URL,
        'logo_url': f'{settings.FRONTEND_URL}/logo-email.png',
        'tagline': 'Travel Smart, Travel Better',
        'phone': '0794333544',
        'email': 'info@akisgroup.net',
        'address': 'Sukaei House, Posta, Dar es Salaam, Tanzania',
        'year': timezone.now().year,
    }
    html_content = render_to_string(template_name, context)
    text_content = render_to_string(template_name.replace('.html', '.txt'), context)

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send(fail_silently=False)
        EmailLog.objects.create(
            recipient=recipient,
            subject=subject,
            body=html_content,
            status=EmailLog.Status.SENT,
        )
        return True
    except Exception as exc:
        logger.exception('Failed to send email to %s: %s', recipient, exc)
        EmailLog.objects.create(
            recipient=recipient,
            subject=subject,
            body=html_content,
            status=EmailLog.Status.FAILED,
            error_message=str(exc),
        )
        return False


def _booking_context(booking):
    return {
        'booking': booking,
        'customer': booking.customer,
        'service': booking.service,
        'budget_display': fmt_budget_range(booking.budget_range),
        'status_display': booking.get_status_display(),
    }


def send_booking_confirmation(booking):
    subject = f'Your Booking Confirmation - {booking.booking_ref}'
    return _send_html_email(
        booking.customer.email,
        subject,
        'emails/booking_confirmation.html',
        _booking_context(booking),
    )


def send_admin_new_booking_alert(booking):
    subject = f'New Booking Received - {booking.booking_ref}'
    return _send_html_email(
        settings.ADMIN_ALERT_EMAIL,
        subject,
        'emails/admin_new_booking.html',
        _booking_context(booking),
    )


def dispatch_booking_emails(booking_id):
    """Send booking notifications in the background so the API responds immediately."""

    def run():
        close_old_connections()
        try:
            from bookings.models import Booking
            from notifications.sms import send_admin_booking_sms

            booking = Booking.objects.select_related('customer', 'service').get(pk=booking_id)
            send_booking_confirmation(booking)
            send_admin_new_booking_alert(booking)
            send_admin_booking_sms(booking)
        except Exception:
            logger.exception('Background booking notification dispatch failed for booking_id=%s', booking_id)
        finally:
            close_old_connections()

    threading.Thread(target=run, daemon=True).start()


def send_status_update(booking):
    subject = f'Booking Update - {booking.booking_ref} is now {booking.get_status_display()}'
    return _send_html_email(
        booking.customer.email,
        subject,
        'emails/status_update.html',
        _booking_context(booking),
    )


def send_contact_acknowledgement(name, email, phone, message):
    context = {'name': name, 'email': email, 'phone': phone, 'message': message}
    customer_subject = 'Thank you for contacting Smart Travels by HL'
    admin_subject = f'New Contact Enquiry from {name}'

    _send_html_email(email, customer_subject, 'emails/contact_acknowledgement.html', context)
    _send_html_email(
        settings.ADMIN_ALERT_EMAIL,
        admin_subject,
        'emails/contact_admin.html',
        context,
    )
