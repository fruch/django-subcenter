from django.contrib import admin
from utils import models

class GenreAdmin(admin.ModelAdmin):
	pass
    
admin.site.register(models.Genre, GenreAdmin)