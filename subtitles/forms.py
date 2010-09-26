from subtitles.models import Subtitle
from django import forms
from formfieldset.forms import FieldsetMixin
from django.forms.widgets import HiddenInput

try:
    from django.utils.translation import ugettext_lazy as _
except:
    # if this fails then _ is a builtin
    pass
    
class SubtitleForm(forms.ModelForm, FieldsetMixin):
    fieldsets = (
                (_('Details'),
                  {'fields': ('version','trasnlated_by'), }),
                )
    
    class Meta:
        model = Subtitle
    def __init__(self, *args, **kwrds):
        super(ActorForm,self).__init__(*args, **kwrds)
        self.fields['origin'].widget = HiddenInput()
        
    def clean_name(self):
        version = self.cleaned_data['version']
        if version == '':
            raise forms.ValidationError(_("name can't be empty"))
        try:
            mobie = Subtitle.objects.get(version=version)
        except Subtitle.DoesNotExist:
            return mobie
        raise forms.ValidationError(_('%s already exists') % version )