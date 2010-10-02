# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from movies.models import Movie
from movies.forms import MovieForm
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
import json
from datetime import datetime
from utils.helper import save_poster, add_cast ,add_genre
from utils.imdb_ext import *
from utils.tasks import findMovieByTitleTask, findMovieByIDTask
            
@login_required
def edit(request, slug):
    '''
    Edit movie info
    '''
    movie, created = Movie.objects.get_or_create(slug=slug)
    
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            obj = form.save(commit=False)
            
            if obj.imdb_poster:
                save_poster(obj, obj.imdb_poster)
                add_cast(obj, form.data['cast'], request.user)
                add_genre(obj, form.data['genre'])

            obj.save()
            return HttpResponseRedirect(reverse("movie_item", args=[obj.slug]))
    else:
        form = MovieForm(instance=movie)
        
    template = 'movies/edit.html'
    data = { 'form': form, }
    
    return render_to_response(template, data , context_instance=RequestContext(request))

@login_required
def add(request):
    '''
    Add new movie info
    '''  
    
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.created = datetime.now()
            obj.save()
            if obj.imdb_poster:
                save_poster(obj, obj.imdb_poster)
            try:
                add_cast(obj, form.data['cast'], request.user)
            except:
	         pass
            try:
                add_genre(obj, form.data['genre'])
            except:
	         pass    
            obj.save()
            return HttpResponseRedirect(reverse("movie_item", args=[obj.slug]))
    else:
        form = MovieForm()
        
    template = 'movies/edit.html'
    data = { 'form': form, }
    
    return render_to_response(template, data , context_instance=RequestContext(request))
    
@login_required
def delete(request, slug):
    '''
    remove movie from db
    '''
    if request.is_ajax():
        movie, created = Movie.objects.get_or_create(slug=slug)
        
        try:
            movie.delete()
            return HttpResponse(json.dumps({'success': True, 'slug':slug}))
        except:
            return HttpResponse(json.dumps({'success': False, 'slug':slug}))
    else:
        raise Http404()
        
@login_required
def imdb_get_info(request, format, movie_id):
    '''
    search a movie in imdb by it's id
    '''
    if request.is_ajax():
        info = {}
        task = findMovieByIDTask.delay(movie_id)
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
    search a movie in imdb by title, and send back a list with names & imdb ids
    '''
    if request.is_ajax():
        info = {}
        task = findMovieByTitleTask.delay(title, filter=None)
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
        


