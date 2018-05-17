from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from vsdk.service_development.models import (MessagePresentation, VoiceLabel, Choice,
                                             VoiceServiceElement)


class PollDurationPresentation(MessagePresentation):
    _urls_name = 'polls:poll-duration-presentation'

    days_label = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('Days label'),
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

    _no_active_poll_redirect = models.ForeignKey(
        VoiceServiceElement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name=_('No active poll redirect element'),
        help_text=_("The element to redirect to after the message has been played,"
                    "and there's no active poll."))

    @property
    def no_active_poll_redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        if self._no_active_poll_redirect:
            return VoiceServiceElement.objects.get_subclass(id=self._no_active_poll_redirect.id)
        else:
            return None

    def validator(self):
        errors = super().validator()

        if not self.days_label:
            errors.append(ugettext('No minutes label is present'))

        if not self.no_active_poll_label:
            errors.append(ugettext('No label for no active poll is present'))

        if not self.final_element and not self._no_active_poll_redirect:
            errors.append(ugettext('No "no active poll" redirect element and '
                                   'this is not a final element'))

        return errors


class PollResultsPresentation(MessagePresentation):
    _urls_name = 'polls:poll-results'

    in_previous_vote_label = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('No active poll label'),
        related_name='+',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    _no_active_poll_redirect = models.ForeignKey(
        VoiceServiceElement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name=_('No active poll redirect element'),
        help_text=_("The element to redirect to after the message has been played,"
                    "and there's no active poll."))

    @property
    def no_active_poll_redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        if self._no_active_poll_redirect:
            return VoiceServiceElement.objects.get_subclass(id=self._no_active_poll_redirect.id)
        else:
            return None

    def validator(self):
        errors = super().validator()

        if not self.in_previous_vote_label:
            errors.append(ugettext('No label for "in previous vote" is present'))

        if not self.final_element and not self._no_active_poll_redirect:
            errors.append(ugettext('No "no active poll" redirect element and '
                                   'this is not a final element'))

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

