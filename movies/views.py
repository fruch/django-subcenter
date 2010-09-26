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
        try:
            movie, ok = do_long_imdb_operation(getmovie_by_id, args=movie_id, timeout=4)
            
            try: info['title'] = movie['title']
            except KeyError: pass
            
            try: info['plot'] = movie['plot'][0]
            except KeyError: pass
            
            try: info['rating'] = movie['rating']
            except KeyError:  pass
            
            try: info['cover_url'] = movie['cover url'] 
            except KeyError: pass
            
            try: info['imdb_url'] = "http://www.imdb.com/title/tt"+movie_id+"/"
            except KeyError: pass
            
            try :  info['year'] = movie['year']
            except KeyError: pass
            
            try : 
                # load seven first actors
                info['cast']  = str(json.dumps([ {'id':x.personID, 'name':x['long imdb name']} for x in movie['cast'] ][0:7]))
            except KeyError: pass
            
            try :  info['genre'] = str(json.dumps([str(m) for m in movie['genres']]))
            except KeyError: pass
            
        except:
            info['error'] = True
            
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
        try:
            movies, ok = do_long_imdb_operation(search_movie_by_title, args=title, timeout=10)
            #get only movies
            info['list'] = [{'id':x.movieID, 'title':x['long imdb canonical title']} for x in movies if x['kind']=='movie']
        except:
            info['error'] = True
            
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
        


