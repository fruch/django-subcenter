from django.contrib import admin
from movies import models

class MovieAdmin(admin.ModelAdmin):
	pass

admin.site.register(models.Movie, MovieAdmin)
