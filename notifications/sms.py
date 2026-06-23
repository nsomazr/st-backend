import base64
import json
import logging
import re

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

BEEM_SMS_URL = 'https://apisms.beem.africa/v1/send'


def normalize_tz_phone(phone):
    """Format phone for Beem Africa (255XXXXXXXXX)."""
    digits = re.sub(r'\D', '', str(phone))
    if digits.startswith('0'):
        return '255' + digits[1:]
    if digits.startswith('255'):
        return digits
    return '255' + digits


def send_beem_sms(phone_number, message):
    api_key = settings.BEEM_SMS_API_KEY
    secret_key = settings.BEEM_SMS_SECRET_KEY

    if not api_key or not secret_key:
        logger.warning('Beem SMS credentials not configured; skipping SMS to %s', phone_number)
        return False

    dest = normalize_tz_phone(phone_number)
    post_data = {
        'source_addr': settings.BEEM_SMS_SOURCE_ADDR,
        'encoding': 0,
        'schedule_time': '',
        'message': message,
        'recipients': [{'recipient_id': '1', 'dest_addr': dest}],
    }
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{api_key}:{secret_key}'.encode()).decode(),
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(
            BEEM_SMS_URL,
            headers=headers,
            data=json.dumps(post_data),
            timeout=15,
            verify=settings.BEEM_SMS_VERIFY_SSL,
        )
        data = response.json()
        if data.get('successful'):
            logger.info('Beem SMS sent to %s', dest)
            return True
        logger.error('Beem SMS failed for %s: %s', dest, data)
        return False
    except Exception as exc:
        logger.exception('Beem SMS error for %s: %s', dest, exc)
        return False


def send_admin_booking_sms(booking):
    """Notify all admin phones about a new booking."""
    message = (
        f"New booking {booking.booking_ref}: "
        f"{booking.customer.full_name} to {booking.destination}, "
        f"travel {booking.travel_date}. "
        f"Call {booking.customer.phone}"
    )

    sent = False
    for phone in settings.ADMIN_ALERT_PHONES:
        if send_beem_sms(phone, message):
            sent = True
    return sent
