from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from vsdk.service_development.models import MessagePresentation, VoiceLabel, Choice


class PollDurationPresentation(MessagePresentation):
    _urls_name = 'polls:poll-duration-presentation'

    minutes_label = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('Minutes label'),
        related_name='+',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    no_active_poll_label = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('No active poll label'),
        related_name='+',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def validator(self):
        errors = super().validator()

        if not self.minutes_label:
            errors.append(ugettext('No minutes label is present'))

        if not self.no_active_poll_label:
            errors.append(ugettext('No label for no active poll is present'))

        return errors


class PollResultsPresentation(MessagePresentation):
    _urls_name = 'polls:poll-results'

    no_active_poll_label = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('No active poll label'),
        related_name='+',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def validator(self):
        errors = super().validator()

        if not self.no_active_poll_label:
            errors.append(ugettext('No label for no active poll is present'))

        return errors


class AskPollDuration(MessagePresentation):
    _urls_name = 'polls:ask-poll-duration'


class ConfirmPollDuration(Choice):
    _urls_name = 'polls:confirm-poll-duration'

    days_correct_label = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('"Days correct" label'),
        related_name='+',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def validator(self):
        errors = super().validator()

        if not self.days_correct_label:
            errors.append(ugettext('No "days correct" label is present'))

        return errors


class CreatePoll(MessagePresentation):
    _urls_name = 'polls:create-poll'


class ConfirmPollCreation(MessagePresentation):
    days_label = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('Days label'),
        related_name='+',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def validator(self):
        errors = super().validator()

        if not self.days_label:
            errors.append(ugettext('No days label is present'))

        return errors


class EndPoll(MessagePresentation):
    _urls_name = 'polls:end-poll'

