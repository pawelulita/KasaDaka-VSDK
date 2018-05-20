from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from vsdk.service_development.models import (MessagePresentation, VoiceLabel, Choice,
                                             VoiceServiceElement)

class NumberPresentation(MessagePresentation):
    _urls_name = 'nums:generate-number'
