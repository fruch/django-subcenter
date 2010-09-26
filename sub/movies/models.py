# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from utils.models import Genre , not_null_not_blank
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from userprofile.countries import CountryField
import os
from transmeta import TransMeta
from tagging.fields import TagField
from persons.models import Actor

#from djangoratings import RatingField

from django.utils.translation import ugettext_lazy as _ 
    
def get_image_posters_path(instance, filename):
    return os.path.join('posters', instance.slug, filename)

class Movie(models.Model):
    __metaclass__ = TransMeta
    
    title = models.CharField(verbose_name=_("The title"),
                                blank=False, null=True, max_length=250)
                               
    slug = models.SlugField(max_length=50, unique=True, blank=False, null=True)
    
    summary = models.TextField(verbose_name=_("The summary"),
                                    blank=False, null=True)
                                    
    publish_year = models.PositiveIntegerField(verbose_name=_("Publish year"), blank=True, null=True)
    
    creator = models.ForeignKey(User, verbose_name=_("Created by"),
                                blank=False, null=True)
    created = models.DateTimeField(verbose_name=_("Created at"),
                                   auto_now_add=True)
    
    #imdb info 
    imdb_url = models.URLField(verbose_name=_("IMDB Url"),verify_exists=False, blank=True, null=True)
    imdb_id = models.PositiveIntegerField(verbose_name=_("IMDB id"), blank=True, null=True)
    imdb_rating = models.DecimalField(verbose_name=_("IMDB Rating"), max_digits=4, decimal_places=2, blank=True, null=True)
    imdb_poster = models.URLField(verbose_name=_("IMDB Poster"),verify_exists=False, blank=True, null=True)
    genre = models.ManyToManyField(Genre, verbose_name=_("Genre"), blank=False, null=True, related_name='movies_in_genre')
    
    
    poster = models.ImageField(verbose_name=_("Poster"), upload_to=get_image_posters_path, blank=True, null=True)
    
    #rating = RatingField(range=5)
    
    # a fixed list of a changeable ?
    #lang =
    country = CountryField(verbose_name=_("Country"), null=True, blank=True)
    
    cast =  models.ManyToManyField(Actor, verbose_name=_("Cast"), null=True, blank=True, related_name='movie_acted_in')
    #producer =
    
    tags = TagField(verbose_name=_("Tags"))
        
        
    class Meta:
        translate = ('title', 'summary' )
        
    def save(self, *args, **kwargs):
        self.slug = slugify(getattr(self, 'title_en'))
        not_null_not_blank(self,('title_en', 'slug' ))
        super(Movie, self).save(*args, **kwargs)  
    
    
    def get_absolute_url(self):
        return reverse("movie_item", args=[self.slug])
    
    def __unicode__(self):
        # note that you can use name and description fields as usual
        return self.title

    def __str__(self):
        # compatibility
        return self.__unicode__()
    
    def imdb_rating_precentage(self):
        ''' retrun a percentage for the visual bar '''
        return str(self.imdb_rating  * 10 )