from django.db import models
from transmeta import TransMeta
from django.utils.translation import ugettext_lazy as _ 

class Genre(models.Model):
    ''' Genre is used both in Movie and in Show'''
    __metaclass__ = TransMeta
    name = models.CharField(verbose_name=_("Name"),
                                blank=False, null=True, max_length=250)
                                
    class Meta:
        translate = ('name',  )
        
    def __unicode__(self):
        # note that you can use name and description fields as usual
        return self.name

    def __str__(self):
        # compatibility
        return self.__unicode__() 


from django.db import IntegrityError
def not_null_not_blank(instance, attribute_name_iter ):
    for attribute_name in attribute_name_iter:
        if not getattr(instance, attribute_name):
            raise IntegrityError('%s.%s may not be NULL or BLANK' % (instance.__class__.__name__, attribute_name )) #This line is inspired by Nattapon (@wrongite)               
        
