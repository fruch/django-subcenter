from django.contrib import admin
from subtitles.models import *

class SubtitleAdmin(admin.ModelAdmin):
	pass
    
admin.site.register(Subtitle, SubtitleAdmin)
