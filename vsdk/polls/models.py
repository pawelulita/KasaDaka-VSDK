from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from vsdk.service_development.models import KasaDakaUser


class Poll(models.Model):
    """
    Polls in our system are represented by this model.
    """
    owner = models.ForeignKey(KasaDakaUser, on_delete=models.PROTECT, null=False)
    start_date = models.DateTimeField(blank=False, null=False)
    duration = models.DurationField(blank=False, null=False)


class Vote(models.Model):
    """
    Votes are represented by this model.
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=False)
    voter = models.ForeignKey(KasaDakaUser, on_delete=models.CASCADE, null=False)
    vote_option = models.ForeignKey('VoteOption', on_delete=models.PROTECT, null=False)
    created = models.DateTimeField(blank=False, auto_now_add=True)


class VoteOption(models.Model):
    """
    Vote options are represented by this model.

    TODO: Add some integration for actual phone numbers.
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=False)
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9)])
