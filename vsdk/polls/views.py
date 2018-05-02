from typing import List

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404

from vsdk.polls.models.custom_elements import PollDurationPresentation
from vsdk.service_development.models import CallSession, Language


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

    context = {
        'prefix_url': element.get_voice_fragment_url(session.language),
        'number_urls': [],  # TODO: Put something here
        'minutes_url': element.minutes_label.get_voice_fragment_url(session.language),
        'redirect_url': redirect_url
    }

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
