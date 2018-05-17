from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.translation import ugettext_lazy as _

from vsdk.service_development.admin import MessagePresentationAdmin
from .models import (PollDurationPresentation, PollResultsPresentation, Poll, VoteOption, Vote,
                     AskPollDuration)


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


class VoteOptionsInLine(admin.TabularInline):
    model = VoteOption


class PollAdmin(ModelAdmin):
    inlines = [VoteOptionsInLine]
    change_form_template = 'admin_edit_poll.html'


admin.site.register(Poll, PollAdmin)
admin.site.register(VoteOption)
admin.site.register(Vote)
admin.site.register(AskPollDuration)
