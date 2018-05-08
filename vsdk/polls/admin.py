from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from vsdk.polls.models import PollDurationPresentation, PollResultsPresentation
from vsdk.service_development.admin import MessagePresentationAdmin


class PollDurationPresentationAdmin(MessagePresentationAdmin):
    fieldsets = MessagePresentationAdmin.fieldsets + [
        (_('Minutes label'), {'fields': ['minutes_label', 'no_active_poll_label']})
    ]


class PollResultsPresentationAdmin(MessagePresentationAdmin):
    fieldsets = MessagePresentationAdmin.fieldsets + [
        (None, {'fields': ['no_active_poll_label']})
    ]


admin.site.register(PollDurationPresentation, PollDurationPresentationAdmin)
admin.site.register(PollResultsPresentation, PollResultsPresentationAdmin)
