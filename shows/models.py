from django.db import models
from persons.models import Actor
from subtitles.models import Subtitle
from transmeta import TransMeta
from tagging.fields import TagField
from utils.models import Genre , not_null_not_blank
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
import os
from django.utils.translation import ugettext_lazy as _
    
def get_image_posters_path(instance, filename):
    return os.path.join('show-posters', instance.slug, filename)
    
class Show(models.Model):
    __metaclass__ = TransMeta
    
    #main fields
    title = models.CharField(verbose_name=_("The title"),
                                blank=False, null=True, max_length=250)
                               
    slug = models.SlugField(max_length=50, unique=True, blank=False, null=True)
    
    summary = models.TextField(verbose_name=_("The summary"),
                                    blank=False, null=True)
    
    poster = models.ImageField(verbose_name=_("Poster"), upload_to=get_image_posters_path, blank=True, null=True)
    
    genre = models.ManyToManyField(Genre, verbose_name=_("Genre"), blank=False, null=True, related_name='shows_in_genre')
    
    cast =  models.ManyToManyField(Actor, verbose_name=_("Cast"), null=True, blank=True, related_name='shows_acted_in')
    
    years = models.CharField(verbose_name=_("Running Years"), blank=False, null=True, max_length=50)
    
    #imdb fields
    
    imdb_id = models.PositiveIntegerField(verbose_name=_("IMDB id"), blank=True, null=True)
    imdb_rating = models.DecimalField(verbose_name=_("IMDB Rating"), max_digits=4, decimal_places=2, blank=True, null=True)
    imdb_poster = models.URLField(verbose_name=_("IMDB Poster"),verify_exists=False, blank=True, null=True)
    
    #admin fields
    creator = models.ForeignKey(User, verbose_name=_("Created by"),
                                blank=False, null=True)
    created = models.DateTimeField(verbose_name=_("Created at"),
                                   auto_now_add=True)                                
    tags = TagField(verbose_name=_("Tags"))
    #rating = RatingField(range=5)
    
    class Meta:
        translate = ('title', 'summary' )
    
    def save(self, *args, **kwargs):
        self.slug = slugify(getattr(self, 'title_en'))
        not_null_not_blank(self,('title_en', 'slug' ))
        super(Show, self).save(*args, **kwargs)  
    
    
    def get_absolute_url(self):
        return reverse("show_item", args=[self.slug])
    
    def __unicode__(self):
        # note that you can use name and description fields as usual
        return self.title

    def __str__(self):
        # compatibility
        return self.__unicode__()
        
    def imdb_url(self):
        if not (self.imdb_id == None):
            return 'http://www.imdb.com/title/tt' + str(self.imdb_id)
        else :
            return '#'
            
    def imdb_rating_precentage(self):
        ''' retrun a percentage for the visual bar '''
        return str(self.imdb_rating  * 10 )
    
    def seasons_orderd(self):
        return self.seasons.order_by('season_num')
        
class Season(models.Model):
    title = models.CharField(verbose_name=_("The title"),
                                blank=False, null=True, max_length=250)
    part_of = models.ForeignKey(Show, verbose_name=_("Belongs to"),
                                 blank=False, null=False, related_name='seasons')
    
    season_num = models.PositiveIntegerField(verbose_name=_("Season Number"), blank=True, null=True)
    
    def __unicode__(self):
        # note that you can use name and description fields as usual
        return u'' + self.part_of.title + u' S' + unicode(self.season_num)

    def __str__(self):
        # compatibility
        return self.__unicode__()
        
    def get_absolute_url(self):
        return reverse("season_item", args=[self.part_of.slug, "%02d" % self.season_num])
        
class Episode(models.Model):
    __metaclass__ = TransMeta
    title = models.CharField(verbose_name=_("The title"),
                                blank=False, null=True, max_length=250)
    summary = models.TextField(verbose_name=_("The summary"),
                                    blank=False, null=True)
    
    slug = models.SlugField(max_length=50, unique=False, blank=False, null=True)
    
    episode_num = models.PositiveIntegerField(verbose_name=_("Episode Number"), blank=True, null=True)    
    
    part_of = models.ForeignKey(Season, verbose_name=_("Belongs to"),
                                 blank=False, null=False, related_name='episodes')
                                 
    subtitles = models.ManyToManyField(Subtitle, verbose_name=_("Substitles"), null=True, blank=True, related_name='subtitle_of')
    
    class Meta:
        translate = ('title', 'summary' )
        
    def get_absolute_url(self):
        return reverse("episode_item", args=[self.part_of.part_of.slug, 
                                             "%02d" % self.part_of.season_num, 
                                             "%02d-%s" % (self.episode_num,self.slug),
                                             ])
    
    def save(self, *args, **kwargs):
        self.slug = slugify(getattr(self, 'title_en'))
        not_null_not_blank(self,('title_en', 'slug' ))
        super(Episode, self).save(*args, **kwargs) 
        
    def __unicode__(self):
        # note that you can use name and description fields as usual
        return u'' + str(self.part_of) + u'E' + unicode(self.episode_num) + ' "' + self.title +'"'

    def __str__(self):
        # compatibility
        return self.__unicode__()