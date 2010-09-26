import os
import json
import urllib
from utils.models import Genre
from persons.models import Actor
from urlparse import urlparse
from django.core.files import File
from utils.tasks import fillActorDataTask
def save_poster(obj, url):
    '''
    Download a poster from imdb url, and save it in poster field in a show/movie
    '''
    f = urllib.urlretrieve(url)
    filetype = urlparse(url).path.split('/')[-1].split('.')[-1]
    filename = "poster."+filetype
    try:
        os.remove(obj.poster.path)
    except:
        pass
    obj.poster.save(filename, File( open(f[0], 'rb') ), save=True)

def add_cast(obj, cast_text , user):
    '''
    Add cast to a show/movie from a a json object.
    '''
    cast = json.loads(cast_text)
    #check if it's not a dict
    if not isinstance(cast[0], int): obj.cast.clear()
    for actor in cast:
        try:
            act, created = Actor.objects.get_or_create(name_en=actor['name'], imdb_id=actor['id'])

            if created:
                act.creator = user
            act.save()
            fillActorDataTask.delay(actor['id'], save_to_db=True)
            obj.cast.add(act)

        except:
            pass

def add_genre(obj, genre_text):
    '''
    Add genre to a show/movie from a a json object.
    '''
    genres = json.loads(genre_text)
    if not isinstance(genres[0], int): obj.genre.clear()
    for genre in genres:
        try:
            if not isinstance(genre, int):
                gen, created = Genre.objects.get_or_create(name_en=genre)
                he_genre = translate_with_wiki('he', genre)
                if he_genre != '':
                    gen.name_he = he_genre
                obj.genre.add(gen)
        except:
            print "error in adding genre"
            pass


def translate_with_wiki(lang, name):
    from wikitools import wiki
    from wikitools import api
    import re

    regex = r"\[\["+lang+r":(?P<name>.*?[^\]])\]\]"

    site = wiki.Wiki()
    site.setMaxlag(20)
    params = {'action':'query', 'export':'on','titles':name}
    request = api.APIRequest(site, params)
    result = request.query()

    text = unicode(result['query']['export'])

    translate_name = None
    found = re.search(regex, text, re.UNICODE | re.DOTALL)
    if found is not None:
        translate_name = found.group("name")

    return translate_name