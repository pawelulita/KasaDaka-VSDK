from datetime import timedelta

from django.http import HttpResponse, HttpRequest, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from vsdk.polls.exceptions import NoCallerIDError
from vsdk.polls.models import (VoteOption, Vote, Poll, PollResultsPresentation,
                               AskPollDurationConfirmation, CreatePoll, ConfirmPollCreation,
                               EndPoll,
                               AskPollDuration)
from vsdk.polls.models.custom_elements import PollDurationPresentation
from vsdk.service_development.models import CallSession, VoiceService, Language
from vsdk.service_development.views import choice_generate_context


def poll_duration_presentation(request: HttpRequest,
                               element_id: int,
                               session_id: int
                               ) -> HttpResponse:
    """
    Take the current active vote for the current user, and communicate its duration.
    In case there's no active vote, communicate this fact.
    """
    element = get_object_or_404(PollDurationPresentation, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(element)

    language: Language = session.language

    poll = getattr(element.service, 'poll', None)
    redirect_url = None

    # There's an active poll
    if poll and poll.active:
        prefix_url = element.get_voice_fragment_url(language)
        number_urls = language.generate_number(poll.remaining_days)
        days_url = element.days_label.get_voice_fragment_url(language)

        audio_urls = [prefix_url] + number_urls + [days_url]

        if not element.final_element and element.redirect:
            redirect_url = element.redirect.get_absolute_url(session)

    # Anything else (e.g. no active poll, no user attached to this session)
    else:
        audio_urls = [element.no_active_poll_label.get_voice_fragment_url(language)]

        if not element.final_element and element.no_active_poll_redirect:
            redirect_url = element.no_active_poll_redirect.get_absolute_url(session)

    context = {
        'audio_urls': audio_urls,
        'redirect_url': redirect_url
    }

    return render(request, 'multi_audio_message.xml', context, content_type='text/xml')


def handle_bip(request: HttpRequest, voice_service_id: int) -> HttpResponse:
    """
    Handle an incoming bip.

    As we have access to only one number (3 May), bips are assigned to vote
    options randomly. It can be misleading, but simulates the real situation
    well enough.

    This view requires a `callerid` in GET parameters. If it's not the case,
    NoCallerIDError (a subclass of Http404) is thrown.

    It also requires the voice service to be active. If it's not active,
    Http404 is thrown.

    TODO: Stop assigning vote options randomly
    """
    caller_id = request.GET.get('callerid', None)

    if not caller_id:
        raise NoCallerIDError()
    else:
        caller_id = caller_id.strip()

    voice_service = get_object_or_404(VoiceService, pk=voice_service_id)

    if not voice_service.active:
        raise Http404()

    # We're taking a random vote option, because we don't have access to multiple numbers yet
    vote_option = VoteOption.objects.filter(poll__voice_service=voice_service).order_by('?').first()

    Vote.objects.create(caller_id=caller_id, vote_option=vote_option)

    return HttpResponse(status=204)


def poll_results(request: HttpRequest, element_id: int, session_id: int) -> HttpResponse:
    """
    Take the current active poll for the current voice service, and present its results.
    In case there's no active poll, communicate this fact.
    """
    element = get_object_or_404(PollResultsPresentation, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(element)

    language: Language = session.language

    poll: Poll = getattr(element.service, 'poll', None)

    if not poll or not poll.active:
        poll = Poll.objects.order_by('-start_date').first()

    redirect_url = None

    if poll:
        audio_urls = []

        if not poll.active:
            audio_urls.append(element.in_previous_vote_label.get_voice_fragment_url(language))

        for vote_result in poll.count_votes():
            count_urls = language.generate_number(vote_result.vote_count)
            audio_urls.extend(count_urls)

            voted_for_url = element.get_voice_fragment_url(language)
            audio_urls.append(voted_for_url)

            value_urls = language.generate_number(vote_result.vote_value)
            audio_urls.extend(value_urls)

        if not element.final_element and element.redirect:
            redirect_url = element.redirect.get_absolute_url(session)

    # If there's no previous poll, we don't say anything
    else:
        audio_urls = []

        if not element.final_element and element.no_active_poll_redirect:
            redirect_url = element.no_active_poll_redirect.get_absolute_url(session)

    context = {
        'audio_urls': audio_urls,
        'redirect_url': redirect_url
    }

    return render(request, 'multi_audio_message.xml', context, content_type='text/xml')


def ask_poll_duration(request: HttpRequest, element_id: int, session_id: int) -> HttpResponse:
    """
    Ask for the duration of a poll, and redirect to the confirmation element.
    """
    element = get_object_or_404(AskPollDuration, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(element)

    if not element.final_element and element.redirect:
        redirect_url = element.redirect.get_absolute_url(session)
    else:
        redirect_url = None

    context = {
        'label_url': element.get_voice_fragment_url(session.language),
        'redirect_url': redirect_url
    }
    return render(request, 'ask_poll_duration.xml', context, content_type='text/xml')


def ask_poll_duration_confirmation(request: HttpRequest,
                                   element_id: int,
                                   session_id: int
                                   ) -> HttpResponse:
    """
    Confirm the duration of a poll.

    To both choice options the duration is sent as a GET parameter.
    """
    element = get_object_or_404(AskPollDurationConfirmation, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(element)

    language: Language = session.language

    duration = int(request.GET['duration'])  # in days

    context = choice_generate_context(element, session)
    context.update({
        'duration': duration,
        'duration_audio_urls': language.generate_number(duration),
        'days_url': element.days_label.get_voice_fragment_url(language),
        'duration_correct_url': element.duration_correct_label.get_voice_fragment_url(language)
    })

    return render(request, 'confirm_poll_duration.xml', context, content_type='text/xml')


def create_poll(request: HttpRequest, element_id: int, session_id: int) -> HttpResponse:
    """
    Create a new poll, and attach it to the current voice service.

    Then, redirect to the next element (possibly confirmation).
    """
    element = get_object_or_404(CreatePoll, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(element)

    Poll.objects.filter(voice_service=session.service).update(voice_service=None)

    duration = int(request.GET['duration'])  # in days
    poll = Poll.objects.create(voice_service=session.service, start_date=timezone.now(),
                               duration=timedelta(days=duration))
    VoteOption.objects.create(poll=poll, value=1)
    VoteOption.objects.create(poll=poll, value=2)

    if not element.final_element and element.redirect:
        redirect_url = element.redirect.get_absolute_url(session)
    else:
        redirect_url = None

    context = {
        'audio_urls': [],
        'redirect_url': redirect_url
    }
    return render(request, 'multi_audio_message.xml', context, content_type='text/xml')


def confirm_poll_created(request: HttpRequest, element_id: int, session_id: int) -> HttpResponse:
    """
    Confirm the duration of a freshly created poll.
    """
    element = get_object_or_404(ConfirmPollCreation, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(element)

    poll: Poll = session.service.poll
    language: Language = session.language

    audio_urls = [element.get_voice_fragment_url(language)]
    audio_urls.extend(language.generate_number(poll.duration.days))
    audio_urls.append(element.days_label.get_voice_fragment_url(language))

    if not element.final_element and element.redirect:
        redirect_url = element.redirect.get_absolute_url(session)
    else:
        redirect_url = None

    context = {
        'audio_urls': audio_urls,
        'redirect_url': redirect_url
    }
    return render(request, 'multi_audio_message.xml', context, content_type='text/xml')


def end_poll(request: HttpRequest, element_id: int, session_id: int) -> HttpResponse:
    """
    End the current poll.
    """
    element = get_object_or_404(EndPoll, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(element)

    Poll.objects.filter(voice_service=session.service).update(voice_service=None)

    if not element.final_element and element.redirect:
        redirect_url = element.redirect.get_absolute_url(session)
    else:
        redirect_url = None

    context = {
        'audio_urls': [],
        'redirect_url': redirect_url
    }
    return render(request, 'multi_audio_message.xml', context, content_type='text/xml')


def votes_json(request: HttpRequest, poll_id: int) -> HttpResponse:
    """
    Get the votes for a poll in a JSON format.

    Example:
    {
        "options": [1, 2, 3],
        "votes": [
            {"id": 1, "nr": "+31611490678", "option": 1, "time": 1526034800000},
            {"id": 2, "nr": "+31611490678", "option": 2, "time": 1526034800001},
            {"id": 3, "nr": "+31611490679", "option": 2, "time": 1526034800002},
        ]
    }

    `options` contains all possible options vor this poll, and `time` is a Unix timestamp.
    """
    poll = get_object_or_404(Poll, pk=poll_id)
    votes = Vote.objects.filter(vote_option__poll=poll).prefetch_related('vote_option')

    results = {
        'options': [vo.value for vo in poll.vote_options.all()],
        'votes': [
            {
                'id': vote.id,
                'nr': vote.caller_id,
                'option': vote.vote_option.value,
                'time': int(vote.created.timestamp())
            }
            for vote in votes
        ]
    }

    return JsonResponse(results)
