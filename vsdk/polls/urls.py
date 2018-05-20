from django.conf.urls import url

from .views import (handle_bip, poll_results, ask_poll_duration, ask_poll_duration_confirmation,
                    poll_duration_presentation, create_poll, end_poll, confirm_poll_created,
                    votes_json)

app_name = 'polls'
urlpatterns = [
    url(r'^poll-duration/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$',
        poll_duration_presentation, name='poll-duration-presentation'),
    url(r'^bip/(?P<voice_service_id>[0-9]+)$', handle_bip, name='handle-bip'),
    url(r'^poll-results/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$',
        poll_results, name='poll-results'),
    url(r'^ask-poll-duration/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$',
        ask_poll_duration, name='ask-poll-duration'),
    url(r'^confirm-poll-duration/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$',
        ask_poll_duration_confirmation, name='confirm-poll-duration'),
    url(r'^create-poll/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$',
        create_poll, name='create-poll'),
    url(r'^poll-created/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$',
        confirm_poll_created, name='poll-created'),
    url(r'^end-poll/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$',
        end_poll, name='end-poll'),
    url(r'^votes-json/(?P<poll_id>[0-9]+)$', votes_json, name='votes-json'),
]
