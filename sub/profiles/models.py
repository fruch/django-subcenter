from django.db import models
from userprofile.models import BaseProfile
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import datetime

GENDER_CHOICES = ( ('F', _('Female')), ('M', _('Male')),)

class Profile(BaseProfile):
    firstname = models.CharField(max_length=255, verbose_name=_("First Name"), blank=True)
    surname = models.CharField(max_length=255, verbose_name=_("Last Name"),blank=True)
    gender = models.CharField(max_length=1, verbose_name=_("Gender"),choices=GENDER_CHOICES, blank=True)
    birthdate = models.DateField(default=datetime.date.today(), verbose_name=_("Birth Date") , blank=True)
    url = models.URLField(verbose_name=_("URL"), blank=True)
    about = models.TextField(verbose_name=_("About"), blank=True)