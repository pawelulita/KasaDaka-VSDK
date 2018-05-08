from django.conf.urls import url

from vsdk.polls.views import handle_bip, poll_results
from .views import poll_duration_presentation

app_name = 'polls'
urlpatterns = [
    url(r'^poll-duration/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$',
        poll_duration_presentation, name='poll-duration-presentation'),
    url(r'^bip/(?P<voice_service_id>[0-9]+)$', handle_bip, name='handle-bip'),
    url(r'^poll-results/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$',
        poll_results, name='poll-results'),
]
