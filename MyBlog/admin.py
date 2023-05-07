from django.contrib import admin
from .models import *
import datetime
from django.conf import settings

admin.site.register(BlogPost)
admin.site.register(Comment)
#admin.site.register(Profile)


