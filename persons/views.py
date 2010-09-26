# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from persons.models import Actor
from persons.forms import ActorForm
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files import File
import os
import json
import urllib
from urlparse import urlparse
from datetime import datetime
from imdb import IMDb
from imdb._exceptions import IMDbDataAccessError
from utils.helper import translate_with_wiki
import log
logger = log.get_logger()

def save_mugshot(obj, url):
    '''
    Download a headshot from imdb url, and save it in headshot field for a person
    '''
    f = urllib.urlretrieve(url)
    filetype = urlparse(url).path.split('/')[-1].split('.')[-1]
    filename = "headshot."+filetype
    try:
        os.remove(obj.headshot.path)
    except:
        pass
    obj.headshot.save(filename, File( open(f[0], 'rb') ), save=True)
    
@login_required
def actor_add(request):
    '''
    Add new actor info
    '''  
    
    if request.method == "POST":
        form = ActorForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.created = datetime.now()
            obj.save()
            if obj.imdb_mugshot:
                save_mugshot(obj, obj.imdb_mugshot)
            obj.save()
            return HttpResponseRedirect(reverse("actor_item", args=[obj.slug]))
    else:
        form = ActorForm()
        
    template = 'persons/edit.html'
    data = { 'form': form, }
    
    return render_to_response(template, data , context_instance=RequestContext(request))

def actor_edit(request, slug):
    '''
    Edit actor info
    '''
    actor, created = Actor.objects.get_or_create(slug=slug)
    
    if request.method == "POST":
        form = ActorForm(request.POST, request.FILES, instance=actor)
        if form.is_valid():
            obj = form.save(commit=False)
            #todo handle mugshot
            if obj.imdb_mugshot:
                save_mugshot(obj, obj.imdb_mugshot)
            
            obj.save()
            return HttpResponseRedirect(reverse("actor_item", args=[obj.slug]))
    else:
        form = ActorForm(instance=actor)
        
    template = 'persons/edit.html'
    data = { 'form': form, }
    
    return render_to_response(template, data , context_instance=RequestContext(request))
    
@login_required
def actor_delete(request, slug):
    '''
    remove an actor from db
    '''
    if request.is_ajax():
        actor, created = Actor.objects.get_or_create(slug=slug)
        
        try:
            actor.delete()
            return HttpResponse(json.dumps({'success': True, 'slug':slug}))
        except:
            return HttpResponse(json.dumps({'success': False, 'slug':slug}))
    else:
        raise Http404()

@login_required
def imdb_get_info(request, format, person_id):
    '''
    search a person in imdb by it's id
    '''
    if request.is_ajax():
        
        info = {}
        try:
             # set the socket timeout to 1sec
            import socket 
            socket.setdefaulttimeout(5)
            # max retrys on this request
            MAX_RETRY = 3 
            fetch = True
            retries = 0
            while fetch:
                if retries >= MAX_RETRY: break
                try:
                    retries += 1
                    ia = IMDb('http')
                    person = ia.get_person(person_id)
                    fetch = False
                except socket.timeout: logger.warn("timeout") 
                except IOError: logger.warn("timeout") 
                except IMDbDataAccessError: logger.warn("imdb error")
            
            socket.setdefaulttimeout(None)
            try: info['name'] = person['name'].replace(' - IMDb', '')
            except KeyError: pass
            
            try: info['bio'] = person['mini biography']
            except KeyError: pass
            
            try: info['headshot'] = person['headshot'] 
            except KeyError: pass
            
            try: info['imdb_url'] = "http://www.imdb.com/name/nm"+person_id+"/"
            except KeyError: pass
            
            try :  info['birth_date'] = person.data['birth date']
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
def imdb_search_by_name(request, format, name):
    '''
    search an actor in imdb by title, and send back a list with names & imdb ids
    '''
    if request.is_ajax():
        info = {}
        info['list'] = []
        try:
            ia = IMDb('httpThin')
            actors = ia.search_person(name)
            for actor in actors:
                id = actor.personID
                found_name = actor['long imdb canonical name']
                info['list'].append({'id':id, 'name':found_name })
                
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
def edb_translate_name(request, format, name):
    '''
    translate the actor name into hebrew
    '''
    if request.is_ajax():
        info = {}
        '''
        # set the socket timeout to 1sec
        import socket 
        socket.setdefaulttimeout(1)
        # max retrys on this request
        MAX_RETRY = 3 
        #regex to catch the hebrew name
        regex =r'<div id="title_container">.*?<h1><a.*?>(?P<name>.*?[^<])</a>.*?</div>'
        url="http://www.edb.co.il/find.php?%s"

        params = urllib.urlencode({'s': name.encode('utf-8') })
        logger.debug(url % params) 
        
        fetch = True
        retries = 0
        data = ''
        while fetch:
            if retries >= MAX_RETRY: break
            try: 
                retries += 1
                f = urllib.urlopen(url % params )
                data = f.read()
                fetch = False
            except socket.timeout: pass
            except IOError: pass
        
        #reset 
        socket.setdefaulttimeout(None)
        
        found = re.search(regex, data, re.UNICODE | re.DOTALL)
        if found is not None:
            info['he_name'] = found.group("name")
        else:
            info['error'] = True
        '''
        he_name = translate_with_wiki('he', name)
        if he_name is not None:
            info['he_name'] = he_name.decode('unicode_escape')
        else: 
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