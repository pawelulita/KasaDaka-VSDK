from typing import NamedTuple, Iterable

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, connection

from vsdk.service_development.models import KasaDakaUser


class VoteResult(NamedTuple):
    vote_value: int
    vote_count: int


class Poll(models.Model):
    """
    Polls in our system are represented by this model.
    """
    owner = models.ForeignKey(KasaDakaUser, on_delete=models.PROTECT, null=False)
    start_date = models.DateTimeField(blank=False, null=False)
    duration = models.DurationField(blank=False, null=False)

    def count_votes(self) -> Iterable[VoteResult]:
        """
        Count the valid votes for this poll.

        This means taking only the last votes for each user. The keys of the returned
        dict are the voting options for poll, and the values are the counts for those
        options.
        """
        query = """
            SELECT vo.value AS vote_value, count(vo.value) AS vote_count
            FROM votes AS v1
            LEFT OUTER JOIN votes AS v2
              ON v1.voter_id = v2.voter_id AND v1.created < v2.created
            JOIN vote_options AS vo ON v1.vote_option_id = vo.id
            WHERE v1.poll_id = %s AND v2.voter_id IS NULL
            GROUP BY vo.value
            ORDER BY vo.value ASC
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [self.id])

            for row in cursor.fetchall():
                yield VoteResult(
                    vote_value=row['vote_value'],
                    vote_count=row['vote_count']
                )


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
