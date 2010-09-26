from django import forms
from movies.models import Movie
from formfieldset.forms import FieldsetMixin
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy as _


class MovieForm(forms.ModelForm, FieldsetMixin):
    '''
    Profile Form. Composed by all the Profile model fields.
    '''
    cast = forms.CharField(required=False)
    genre = forms.CharField(required=False)
    fieldsets = (
                
                (_('English'),
                  {'fields': ('title_en','summary_en'), }),
                (_('Hebrew'),
                  {'fields': ('title_he','summary_he'), }),
                (_('Russian'),
                  {'fields': ('title_ru','summary_ru'), }),
                  
                  (_('Movie Details'), {'fields': ('tags', 
                                                   'country',
                                                   'publish_year', 
                                                   'imdb_id', 
                                                   'imdb_url', 
                                                   'imdb_rating',
                                                   'imdb_poster',
                                                   'cast',
                                                   'genre', 
                                                   'poster'),
                   'description': _('Your tags are shared')}),
                )
    
    

    class Meta:
        model = Movie
        exclude = ('slug', 'creator', )
    
    def __init__(self, *args, **kwrds):
        super(MovieForm,self).__init__(*args, **kwrds)
        self.fields['imdb_id'].widget = HiddenInput()
        self.fields['imdb_url'].widget = HiddenInput()
        self.fields['imdb_rating'].widget = HiddenInput()
        self.fields['imdb_poster'].widget = HiddenInput()
        
        self.fields['cast'].widget = HiddenInput()
        self.fields['cast'].value = ''
        
        self.fields['genre'].widget = HiddenInput()
        self.fields['genre'].value = ''
        
    def clean_title(self):
        title = self.cleaned_data['title_en']
        if title == '':
            raise forms.ValidationError(_("title can't be empty"))
        try:
            mobie = Movie.objects.get(title=title)
        except Movie.DoesNotExist:
            return mobie
        raise forms.ValidationError(_('%s already exists') % title )