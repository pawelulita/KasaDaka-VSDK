from django.conf.urls import url

from .views import poll_duration_presentation

app_name = 'polls'
urlpatterns = [
    url(r'^poll-duration/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$',
        poll_duration_presentation, name='poll-duration-presentation'),
]
