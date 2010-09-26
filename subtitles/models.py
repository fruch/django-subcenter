from django.db import models
from django.utils.translation import ugettext_lazy as _
import os
# Create your models here.

def get_subtitles_path(instance, filename):
    return os.path.join('subtitles', instance.version, filename)

class Subtitle(models.Model):
    LANG_CHOICES = (
        (u'EN', _('English')),
        (u'HE', _('Hebrew')),
        (u'RU', _('Russian')),
    )

    version = models.CharField(verbose_name=_("Subtitle Version"),
                                blank=False, null=True, max_length=250)

    trasnlated_by = models.CharField(verbose_name=_("Translate by"),
                                blank=False, null=True, max_length=250)

    sync_by = models.CharField(verbose_name=_("Syncronized by"),
                                blank=False, null=True, max_length=250)
                                
    num_parts = models.DecimalField(verbose_name=_("Number of Parts"), 
                                    max_digits=1, decimal_places=0, blank=True, null=True)
                        
    
    lang = models.CharField(verbose_name=_("Langue"), 
            blank=False, null=True, max_length=2, choices=LANG_CHOICES)
    
    sub_file = models.FileField(verbose_name=_("Subtitle File"), 
        upload_to=get_subtitles_path, blank=True, null=True)  
    