from django.db import models
from transmeta import TransMeta
from tagging.fields import TagField
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
import os
from django.utils.translation import ugettext_lazy as _
 
def get_image_mugshot_path(instance, filename):
    return os.path.join('headshots', instance.slug, filename)
    
class Person(models.Model):
    
    headshot = models.ImageField(verbose_name=_("Headshot"), upload_to=get_image_mugshot_path, blank=True, null=True)  
    
    creator = models.ForeignKey(User, verbose_name=_("Created by"),
                                blank=True, null=True)
    created = models.DateTimeField(verbose_name=_("Created at"),
                                   auto_now_add=True)
                                   
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
    
    imdb_id = models.PositiveIntegerField(verbose_name=_("IMDB id"), blank=True, null=True)
    imdb_mugshot = models.URLField(verbose_name=_("IMDB Mugshot"),verify_exists=False, blank=True, null=True) 
    imdb_url = models.URLField(verbose_name=_("IMDB Url"),verify_exists=False, blank=True, null=True)
    
    tags = TagField()
    
    class Meta:
        abstract = True
        
class Actor(Person):
    __metaclass__ = TransMeta
    
    name = models.CharField(verbose_name=_("Name"),
                    blank=True, null=False, max_length=250)
                                
    bio = models.TextField(verbose_name=_("Biography"),
                                    blank=True, null=False)
                                    
    def get_absolute_url(self):
        return reverse("actor_item", args=[self.slug])
        
    def save(self, *args, **kwargs):
        self.slug = slugify(getattr(self, 'name_en'))
        super(Person, self).save(*args, **kwargs)  
        
    def __unicode__(self):
        # note that you can use name and description fields as usual
        return self.name

    def __str__(self):
        # compatibility
        return self.__unicode__()
        
    class Meta:
        translate = ('name', 'bio' )