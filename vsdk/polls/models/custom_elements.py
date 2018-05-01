from django.db import models
from django.utils.translation import ugettext_lazy as _

from vsdk.service_development.models import MessagePresentation, VoiceLabel


class PollDurationPresentation(MessagePresentation):
    _urls_name = 'polls:poll-duration-presentation'

    minutes_label = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('Minutes label'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
