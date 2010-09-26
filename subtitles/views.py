from django.contrib.auth.decorators import login_required
from subtitles.models import Subtitle
from subtitles.forms import SubtitleForm

@login_required
def edit(request, id):
    '''
    Edit show info
    '''
    show, created = Subtitle.objects.get_or_create(id=id)
    
    if request.method == "POST":
        form = SubtitleForm(request.POST, request.FILES, instance=show)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse("subtitle_item", args=[obj.id]))
    else:
        form = SubtitleForm(instance=show)
        
    template = 'shows/show_edit.html'
    data = { 'form': form, 'edit': True}
    
    return render_to_response(template, data , context_instance=RequestContext(request))

@login_required
def add(request):
    '''
    Add subtitle
    '''  
    
    if request.method == "POST":
        form = SubtitleForm(request.POST, request.FILES)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.created = datetime.now()  
            obj.save()
            return HttpResponseRedirect(reverse("subtitle_item", args=[obj.id]))
    else:
        form = SubtitleForm()
        
    template = 'subtitles/subtitle_edit.html'
    data = { 'form': form, }
    
    return render_to_response(template, data , context_instance=RequestContext(request))