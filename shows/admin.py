from django.contrib import admin
from shows.models import *

class ShowAdmin(admin.ModelAdmin):
	pass

class EpisodeAdmin(admin.ModelAdmin):
	pass
    
class SeasonAdmin(admin.ModelAdmin):
	pass   
    
admin.site.register(Show, ShowAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Season, SeasonAdmin)