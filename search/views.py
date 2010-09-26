# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from movies.models import Movie
from persons.models import Actor

from search.index import complete_indexer
from django import forms

try:
    from django.utils.translation import ugettext_lazy as _
except:
    # if this fails then _ is a builtin
    pass
    
MODEL_MAP = {
    'movie': Movie,
    'actor': Actor,
}

MODEL_CHOICES = [('', 'all')] + zip(MODEL_MAP.keys(), MODEL_MAP.keys())

class SearchForm(forms.Form):
    query = forms.CharField(label=_("Query"), required=True)
    model = forms.ChoiceField(label=_("Type"), choices=MODEL_CHOICES, required=False)
    
def search(request):
    results = []

    if request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            model = MODEL_MAP.get(form.cleaned_data['model'])

            if not model:
                indexer = complete_indexer
            else:
                indexer = model.indexer

            results = indexer.search(query)
            #.prefetch()
            
            print [str(x) for x in results]
    else:
        form = SearchForm()

    return render_to_response('search/search.html', {'results': results, 'form': form}, context_instance=RequestContext(request))