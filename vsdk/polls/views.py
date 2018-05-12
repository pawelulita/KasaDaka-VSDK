from datetime import timedelta
from typing import List

from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from vsdk.polls.exceptions import NoCallerIDError
from vsdk.polls.models import VoteOption, Vote, Poll, PollResultsPresentation, CreatePoll
from vsdk.polls.models.custom_elements import PollDurationPresentation
from vsdk.service_development.models import CallSession, Language, VoiceService


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

    if not element.final_element and element.redirect:
        redirect_url = element.redirect.get_absolute_url(session)
    else:
        redirect_url = None

    poll = getattr(element.service, 'poll', None)

    # There's an active poll
    if poll and poll.active:
        prefix_url = element.get_voice_fragment_url(session.language)
        number_urls = _convert_number_to_audio_urls(poll.remaining_minutes, session.language)
        minutes_url = element.minutes_label.get_voice_fragment_url(session.language)

        audio_urls = [prefix_url] + number_urls + [minutes_url]

    # Anything else (e.g. no active poll, no user attached to this session)
    else:
        audio_urls = [element.no_active_poll_label.get_voice_fragment_url(session.language)]

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

    if not element.final_element and element.redirect:
        redirect_url = element.redirect.get_absolute_url(session)
    else:
        redirect_url = None

    poll: Poll = getattr(element.service, 'poll', None)

    # There's an active poll
    if poll and poll.active:
        audio_urls = []

        for vote_result in poll.count_votes():
            count_urls = _convert_number_to_audio_urls(vote_result.vote_count, session.language)
            audio_urls.extend(count_urls)

            voted_for_url = element.get_voice_fragment_url(session.language)
            audio_urls.append(voted_for_url)

            value_urls = _convert_number_to_audio_urls(vote_result.vote_value, session.language)
            audio_urls.extend(value_urls)

    # Anything else (e.g. no active poll, no user attached to this session)
    else:
        audio_urls = [element.no_active_poll_label.get_voice_fragment_url(session.language)]

    context = {
        'audio_urls': audio_urls,
        'redirect_url': redirect_url
    }

    return render(request, 'multi_audio_message.xml', context, content_type='text/xml')


def create_poll(request: HttpRequest, element_id: int, session_id: int) -> HttpResponse:
    """
    Create a new poll, and attach it to the current voice service.
    """
    element = get_object_or_404(CreatePoll, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(element)

    # We received a request to create a new poll
    if request.method == 'POST':
        old_poll: Poll = getattr(session.service, 'poll', None)

        if old_poll:
            old_poll.voice_service = None
            old_poll.save()

        duration = int(request.POST['duration'])  # in days
        Poll.objects.create(
            voice_service=session.service,
            start_date=timezone.now(),
            duration=timedelta(days=duration)
        )

        if not element.final_element and element.redirect:
            return redirect(element.redirect.get_absolute_url(session))
        else:
            return HttpResponse(status=201)

    else:
        context = {'label_url': element.get_voice_fragment_url(session.language)}
        return render(request, 'poll_duration.xml', context, content_type='text/xml')


def _convert_number_to_audio_urls(num: int, language: Language) -> List[str]:
    """
    Convert a non-negative number to a list of URLs representing its value.

    If the number is negative, it's treated as if it was 0.
    """
    digit_urls = language.get_interface_numbers_voice_label_url_list

    if num <= 0:
        return [digit_urls[0]]

    urls = []

    while num != 0:
        urls.append(digit_urls[num % 10])
        num = num // 10

    urls.reverse()

    return urls
