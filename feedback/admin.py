from django.contrib import admin
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'name', 'email', 'phone', 'call_time')
    list_display_links = ('id', 'name')
    search_fields = ('date', 'name')
    list_filter = ('date', 'name')


admin.site.register(Feedback, FeedbackAdmin)
