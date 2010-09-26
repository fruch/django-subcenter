from django.contrib import admin
from profiles.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('name',)

admin.site.register(Profile, ProfileAdmin)