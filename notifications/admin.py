from django.contrib import admin

from .models import EmailLog


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('subject', 'recipient', 'status', 'sent_at')
    list_filter = ('status',)
    search_fields = ('recipient', 'subject')
    readonly_fields = ('sent_at',)
