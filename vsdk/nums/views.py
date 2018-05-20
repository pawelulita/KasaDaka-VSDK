from random import randint

from django.http import HttpResponse, HttpRequest, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.safestring import mark_safe

from vsdk.nums.models.custom_elements import NumberPresentation
from vsdk.service_development.models import CallSession, Language, VoiceService
from vsdk.service_development.views import choice_generate_context


def generate_number(request: HttpRequest, element_id: int, session_id: int) -> HttpResponse:
    """
    Generate a random number using the current language.
    """
    element = get_object_or_404(NumberPresentation, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(element)

    number = randint(1, 9999)
    audio_urls = session.language.generate_number(number)

    context = {
        'language': session.language,
        'dict': mark_safe(session.language.get_interface_numbers_voice_label_url_dict),
        'number': number,
        'audio_urls': audio_urls
    }

    return render(request, 'number_message.xml', context, content_type='text/xml')
