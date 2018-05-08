from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from vsdk.service_development.models import MessagePresentation, VoiceLabel


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
