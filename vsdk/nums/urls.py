from django.conf.urls import url

from .views import (generate_number)

app_name = 'nums'
urlpatterns = [
    url(r'^generate/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$',
        generate_number, name='generate-number')
]
