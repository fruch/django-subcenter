# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from shows.models import Show, Season, Episode
from shows.forms import ShowForm
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
import json
from datetime import datetime
from utils.helper import *
from utils.imdb_ext import *
from utils.tasks import findMovieByTitleTask, findShowByIDTask, fillShowEpisodesTask
import log
logger = log.get_logger()
            
@login_required
def edit(request, slug):
    '''
    Edit show info
    '''
    show, created = Show.objects.get_or_create(slug=slug)
    
    if request.method == "POST":
        form = ShowForm(request.POST, request.FILES, instance=show)
        if form.is_valid():
            obj = form.save(commit=False)
            
            if obj.imdb_poster:
                save_poster(obj, obj.imdb_poster)
            if form.data['cast'] != '':
                add_cast(obj, form.data['cast'], request.user)
            if form.data['genre'] != '':
                add_genre(obj, form.data['genre'])
            obj.save()
            return HttpResponseRedirect(reverse("show_item", args=[obj.slug]))
    else:
        form = ShowForm(instance=show)
        
    template = 'shows/show_edit.html'
    data = { 'form': form, 'edit': True}
    
    return render_to_response(template, data , context_instance=RequestContext(request))

@login_required
def add(request):
    '''
    Add new show info
    '''  
    
    if request.method == "POST":
        form = ShowForm(request.POST, request.FILES)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.created = datetime.now()
            obj.save()
            if obj.imdb_poster:
                save_poster(obj, obj.imdb_poster)
            if form.data['cast'] != '':
                add_cast(obj, form.data['cast'], request.user)
            if form.data['genre'] != '':
                add_genre(obj, form.data['genre'])    
            obj.save()
            # start the back ground prossess to find all episodes
            fillShowEpisodesTask.delay(obj.title_en)
            return HttpResponseRedirect(reverse("show_item", args=[obj.slug]))
    else:
        form = ShowForm()
        
    template = 'shows/show_edit.html'
    data = { 'form': form, }
    
    return render_to_response(template, data , context_instance=RequestContext(request))
    
@login_required
def delete(request, slug):
    '''
    remove show from db
    '''
    if request.is_ajax():
        show, created = Show.objects.get_or_create(slug=slug)
        
        try:
            show.delete()
            return HttpResponse(json.dumps({'success': True, 'slug':slug}))
        except:
            return HttpResponse(json.dumps({'success': False, 'slug':slug}))
    else:
        raise Http404()
        
@login_required
def imdb_get_info(request, format, show_id):
    '''
    search a show in imdb by it's id
    '''
    if request.is_ajax():
        
        info = {}
        task = findShowByIDTask.delay(show_id)
        info["task_id"] = task.task_id
     
        if format == 'xml':
            mimetype = 'application/xml'
            #TODO xml serialize
            data = 'Not implemented'
        if format == 'json':
            mimetype = 'application/javascript'
            data = json.dumps(info)

        return HttpResponse(data ,mimetype)
    # If you want to prevent non XHR calls
    else:
        return HttpResponse(status=400)

@login_required
def imdb_search_by_title(request, format, title):
    '''
    search a show in imdb by title, and send back a list with names & imdb ids
    '''
    if request.is_ajax():
        info = {}
        task = findMovieByTitleTask.delay(title, filter="tv series")
        info["task_id"] = task.task_id
   
        if format == 'xml':
            mimetype = 'application/xml'
            #TODO xml serialize
            data = 'Not implemented'
        if format == 'json':
            mimetype = 'application/javascript'
            data = json.dumps(info)

        return HttpResponse(data ,mimetype)
    # If you want to prevent non XHR calls    
    else:
        return HttpResponse(status=400)
        

def season_details(request, slug, season_num):
   
    show    = get_object_or_404(Show, slug=slug)
    season  = get_object_or_404(Season, season_num=season_num, part_of=show)
    
    template = 'shows/season_detail.html'
    data = { 'object': season, }
    
    return render_to_response(template, data , context_instance=RequestContext(request))
    
def episode_details(request, slug, season_num, episode_slug):
    
    show    = get_object_or_404(Show, slug=slug)
    season  = get_object_or_404(Season, season_num=season_num, part_of=show)
    num, e_slug  = episode_slug.split('-', 1)
    episode = get_object_or_404(Episode, episode_num=num , slug=e_slug, part_of=season)

        
    template = 'shows/episode_detail.html'
    data = { 'object': episode, }
    
    return render_to_response(template, data , context_instance=RequestContext(request))
    
    
@login_required
def fill_show_episodes(request, format, title):
    '''
    search a show episodes imdb and create all the episode guide for it, return succsuflly or not
    '''
    if request.is_ajax():
        info = {}
        task = fillShowEpisodesTask.delay(title)
        info["task_id"] = task.task_id

        if format == 'xml':
            mimetype = 'application/xml'
            #TODO xml serialize
            data = 'Not implemented'
        if format == 'json':
            mimetype = 'application/javascript'
            data = json.dumps(info)

        return HttpResponse(data ,mimetype)
    # If you want to prevent non XHR calls    
    else:
        return HttpResponse(status=400)
    