from typing import NamedTuple, Iterable

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, connection
from django.utils import timezone

from vsdk.service_development.models import VoiceService


class VoteResult(NamedTuple):
    vote_value: int
    vote_count: int


class Poll(models.Model):
    """
    Polls in our system are represented by this model.
    """
    voice_service = models.OneToOneField(VoiceService, on_delete=models.PROTECT, null=True,
                                         blank=True)
    start_date = models.DateTimeField(blank=False, null=False)
    duration = models.DurationField(blank=False, null=False)

    def count_votes(self) -> Iterable[VoteResult]:
        """
        Count the valid votes for this poll.

        This means taking only the last votes for each user. The keys of the returned
        dict are the voting options for poll, and the values are the counts for those
        options.
        """

        # The inner query takes only the last vote for each voter, and the outer one
        # joins it with possible voting options.
        query = """
            select vo.value as vote_value, count(votes.id) as vote_count
            from polls_voteoption as vo
                left outer join (
                    select v1.*
                    from polls_vote v1
                        left outer join polls_vote v2
                            on v1.caller_id = v2.caller_id and v1.created < v2.created
                    where v2.caller_id is null
                ) as votes on votes.vote_option_id = vo.id
            where vo.poll_id = %s 
            group by vo.value
            order by vo.value asc;
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [self.id])
            rows = cursor.fetchall()

            column_names = [col[0] for col in cursor.description]
            results = [dict(zip(column_names, row)) for row in rows]

            for result in results:
                yield VoteResult(
                    vote_value=result['vote_value'],
                    vote_count=result['vote_count']
                )

    @property
    def active(self) -> bool:
        """
        True if the poll is active, False otherwise.
        """
        return self.voice_service and self.start_date + self.duration > timezone.now()

    @property
    def remaining_days(self) -> int:
        """
        Get the number of remaining full days.
        """
        if not self.active:
            return 0

        remaining = self.start_date + self.duration - timezone.now()
        return remaining.days


class Vote(models.Model):
    """
    Votes are represented by this model.
    """
    caller_id = models.CharField(max_length=100)
    vote_option = models.ForeignKey('VoteOption', on_delete=models.PROTECT, null=False)
    created = models.DateTimeField(blank=False, auto_now_add=True)


class VoteOption(models.Model):
    """
    Vote options are represented by this model.

    TODO: Add some integration for actual phone numbers.
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=False,
                             related_name='vote_options')
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9)])
