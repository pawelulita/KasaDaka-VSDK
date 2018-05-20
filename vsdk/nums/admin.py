from django.contrib import admin
from django.contrib.admin import ModelAdmin

from vsdk.service_development.admin import MessagePresentationAdmin
from .models import (NumberPresentation)

admin.site.register(NumberPresentation, MessagePresentationAdmin)
