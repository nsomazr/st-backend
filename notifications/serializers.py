from rest_framework import serializers

from .models import EmailLog


class EmailLogSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = EmailLog
        fields = (
            'id', 'recipient', 'subject', 'body', 'sent_at',
            'status', 'status_display', 'error_message',
        )
