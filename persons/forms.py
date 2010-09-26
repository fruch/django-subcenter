from django import forms
from persons.models import Actor
from formfieldset.forms import FieldsetMixin
from django.forms.widgets import HiddenInput

try:
    from django.utils.translation import ugettext_lazy as _
except:
    # if this fails then _ is a builtin
    pass


class ActorForm(forms.ModelForm, FieldsetMixin):
    '''
    Actor Form
    '''
    fieldsets = (
                
                (_('English'),
                  {'fields': ('name_en','bio_en'), }),
                (_('Hebrew'),
                  {'fields': ('name_he','bio_he'), }),
                (_('Russian'),
                  {'fields': ('name_ru','bio_ru'), }),

                  (_('Actor Details'), {'fields': ('tags', 'imdb_id', 'imdb_url','imdb_mugshot' ,'headshot'),
                   'description': _('Your tags are shared')}),
                )
    
    class Meta:
        model = Actor
        exclude = ('slug', 'creator', )
    
    def __init__(self, *args, **kwrds):
        super(ActorForm,self).__init__(*args, **kwrds)
        self.fields['imdb_id'].widget = HiddenInput()
        self.fields['imdb_url'].widget = HiddenInput()
        self.fields['imdb_mugshot'].widget = HiddenInput()
    
    def clean_name(self):
        title = self.cleaned_data['name_en']
        if title == '':
            raise forms.ValidationError(_("name can't be empty"))
        try:
            mobie = Actors.objects.get(name=name)
        except Actors.DoesNotExist:
            return mobie
        raise forms.ValidationError(_('%s already exists') % title )