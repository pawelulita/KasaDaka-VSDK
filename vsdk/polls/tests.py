from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from vsdk.polls.models import Poll, VoteOption, Vote, VoteResult
from vsdk.service_development.models import VoiceService


class PollTests(TestCase):
    def setUp(self):
        voice_service = VoiceService.objects.create(
            name='Test VS',
            description='Description',
            active=True,
            registration='disabled'
        )
        self.poll = Poll.objects.create(
            voice_service=voice_service,
            start_date=timezone.now(),
            duration=timedelta(days=10)
        )
        self.vote_option1 = VoteOption.objects.create(poll=self.poll, value=1)
        self.vote_option2 = VoteOption.objects.create(poll=self.poll, value=2)

        self.caller_id1 = '10001'
        self.caller_id2 = '10002'

    def test_bip(self):
        """
        Simulate 2 bips, and check if they were registered as votes.
        """
        response = self.client.get(f'/polls/bip/{self.poll.id}?callerid={self.caller_id1}')
        self.assertEquals(response.status_code, 204)

        response = self.client.get(f'/polls/bip/{self.poll.id}?callerid={self.caller_id1}')
        self.assertEquals(response.status_code, 204)

        vote_count = Vote.objects.filter(caller_id=self.caller_id1).count()
        self.assertEquals(vote_count, 2)

    def test_vote_deduplication(self):
        Vote.objects.create(
            caller_id=self.caller_id1,
            vote_option=self.vote_option1,
            created=timezone.now()
        )
        Vote.objects.create(
            caller_id=self.caller_id2,
            vote_option=self.vote_option1,
            created=timezone.now()
        )
        Vote.objects.create(
            caller_id=self.caller_id1,
            vote_option=self.vote_option2,
            created=timezone.now() + timedelta(days=1)
        )

        vote_counts = set(self.poll.count_votes())
        expected_vote_counts = {
            VoteResult(vote_value=self.vote_option1.value, vote_count=1),
            VoteResult(vote_value=self.vote_option2.value, vote_count=1),
        }

        self.assertEquals(vote_counts, expected_vote_counts)
