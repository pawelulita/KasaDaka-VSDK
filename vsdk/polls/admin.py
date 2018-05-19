from django.contrib import admin
from django.contrib.admin import ModelAdmin

from vsdk.service_development.admin import MessagePresentationAdmin
from .models import (PollDurationPresentation, PollResultsPresentation, Poll, VoteOption, Vote,
                     AskPollDurationConfirmation, CreatePoll, ConfirmPollCreation, EndPoll,
                     AskPollDuration)


class PollDurationPresentationAdmin(MessagePresentationAdmin):
    fieldsets = MessagePresentationAdmin.fieldsets + [
        (None, {'fields': ['days_label', 'no_active_poll_label', '_no_active_poll_redirect']})
    ]


admin.site.register(PollDurationPresentation, PollDurationPresentationAdmin)


class PollResultsPresentationAdmin(MessagePresentationAdmin):
    fieldsets = MessagePresentationAdmin.fieldsets + [
        (None, {'fields': ['in_previous_vote_label', '_no_active_poll_redirect']})
    ]


admin.site.register(PollResultsPresentation, PollResultsPresentationAdmin)


class PollResultsPresentationAdmin(MessagePresentationAdmin):
    fieldsets = MessagePresentationAdmin.fieldsets + [
        (None, {'fields': ['in_previous_vote_label', '_no_active_poll_redirect']})
    ]


admin.site.register(EndPoll, MessagePresentationAdmin)

admin.site.register(AskPollDuration, MessagePresentationAdmin)


class ConfirmPollCreationAdmin(MessagePresentationAdmin):
    fieldsets = MessagePresentationAdmin.fieldsets + [
        (None, {'fields': ['days_label']})
    ]


admin.site.register(ConfirmPollCreation, ConfirmPollCreationAdmin)


class VoteOptionsInLine(admin.TabularInline):
    model = VoteOption


class PollAdmin(ModelAdmin):
    inlines = [VoteOptionsInLine]
    change_form_template = 'admin_edit_poll.html'


admin.site.register(Poll, PollAdmin)
admin.site.register(VoteOption)
admin.site.register(Vote)
admin.site.register(AskPollDurationConfirmation)
admin.site.register(CreatePoll)
