
from celery.registry import tasks
from celery.task import Task
from shows.models import Episode
from shows.models import Season
from shows.models import Show
from utils.imdb_ext import do_long_imdb_operation
from utils.imdb_ext import getmovie_by_id
from utils.imdb_ext import search_movie_by_title
from utils.imdb_ext import search_person_by_name
from utils.imdb_ext import update_episodes
from utils.imdb_ext import getperson_by_id
import json

class findMovieByTitleTask(Task):
    """search a movie/show by it's title, cause use filter on kind (movie, tv series) """
    def run(self, title,  filter=None):
        info = {}
        movie_list, ok = do_long_imdb_operation(search_movie_by_title, args=title, timeout=5)
        if ok:
            if filter is not None:
                info['list'] = [{'id':x.movieID, 'title':x['long imdb canonical title']} for x in movie_list if x['kind']==filter]
            else:
                info['list'] = [{'id':x.movieID, 'title':x['long imdb canonical title']} for x in movie_list]
        else:
            info['error'] = True
        return info

class findPersonByNameTask(Task):
    def run(self, name):
        info = {}
        info['list'] = []
        actors, ok = do_long_imdb_operation(search_person_by_name, args=name, timeout=5)
        if ok:
            for actor in actors:
                id = actor.personID
                found_name = actor['long imdb canonical name']

                info['list'].append({'id':id, 'name':found_name })
        else:
            info['error'] = True

        return info

class findShowByIDTask(Task):
    def run(self, show_id):
        info = {}
        show, ok = do_long_imdb_operation(getmovie_by_id, args=show_id, timeout=4)
        if ok:
            try: info['title'] = show['title']
            except KeyError: pass

            try: info['plot'] = show['plot'][0]
            except KeyError: pass

            try: info['rating'] = show['rating']
            except KeyError:  pass

            try: info['cover_url'] = show['cover url']
            except KeyError: pass

            try :  info['years'] = show['series years']
            except KeyError: pass

            try :
                # load seven first actors
                info['cast']  = str(json.dumps([ {'id':x.personID, 'name':x['long imdb name']} for x in show['cast'] ][0:7]))
            except KeyError: pass

            try :  info['genre'] = str(json.dumps([str(m) for m in show['genres']]))
            except KeyError: pass
        else:
            info['error'] = True
        return info


class fillShowEpisodesTask(Task):
    def run(self, title):
        info = {}

        show = Show.objects.get(title_en=title)

        imdb_show, ok = do_long_imdb_operation(getmovie_by_id, args=show.imdb_id, timeout=4)

        imdb_show, ok = do_long_imdb_operation(update_episodes, args=imdb_show, timeout=10)

        for s in imdb_show['episodes']:
            try:
              season , created = Season.objects.get_or_create(season_num=s, part_of=show)
            except: continue
            for e in imdb_show['episodes'][s]:
                try:  episode_num = imdb_show['episodes'][s][e]['episode']
                except: episode_num = 0

                try:  title = imdb_show['episodes'][s][e]['title']
                except: title = 'No found'

                try: plot = imdb_show['episodes'][s][e]['plot']
                except: plot = 'No found'

                #TODO:
                #air_date = imdb_show['episodes'][s][e]['original air date']
                episode , created = Episode.objects.get_or_create(
                                                                    title_en = title,
                                                                    episode_num=episode_num,
                                                                    part_of=season)
                episode.summary_en = plot
               
                episode.save()
        info['success'] = True
        return info

class fillActorDataTask(Task):
    def run(self, person_id, save_to_db=False,  **kwargs):
        info = {}

        person, ok = do_long_imdb_operation(getperson_by_id, args=person_id, timeout=4)
        if ok:
            try: info['name'] = person['name']
            except KeyError: pass

            try: info['bio'] = person['mini biography'][0]
            except KeyError: pass

            try: info['headshot'] = person['headshot']
            except KeyError: pass

            try: info['imdb_url'] = "http://www.imdb.com/name/nm"+person_id+"/"
            except KeyError: pass

            try :  info['birth_date'] = person.data['birth date']
            except KeyError: pass

            if save_to_db:
                from persons.models import Actor
                from persons.views import save_mugshot
                from utils.helper import translate_with_wiki
                act, created = Actor.objects.get_or_create(name_en=info['name'] )

                try: act.bio_en = unicode(info['bio'])
                except KeyError: pass

                he_name =  translate_with_wiki('he',info['name'])
                if he_name is not None:
                    act.name_he = he_name.decode('unicode_escape')

                ru_name =  translate_with_wiki('ru',info['name'])
                if ru_name is not None:
                    act.name_ru = ru_name.decode('unicode_escape')

                act.imdb_url = unicode(info['imdb_url'])

                try: save_mugshot(act, info['headshot'] )
                except KeyError: pass

                act.save()
        else:
            info['error'] = True

        return info

from celery.task import PeriodicTask
from datetime import timedelta
from django.core.management import call_command
import os
from  shutil import copy

class maintenanceReIndexTask(PeriodicTask):
    """
    run a reindex of djapian each round hour
    """
    run_every = timedelta(minutes=3)

    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Running periodic task!")
        call_command('index',rebuild_index=True)
        return True
        
class maintenanceTranslateTask(PeriodicTask):
    run_every = timedelta(minutes=3)

    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Running periodic task!")
        
        curr = os.getcwd()
        logger.info(curr)
        
        try:
            os.system ("lang_comp.bat 1>> lang_comp.log 2>&1")
            '''
            for m in ['movies', 'persons','shows',  'profiles']:
                os.chdir(m)
                logger.info("calling command "+ m)
                call_command('makemessages',all=True)
                call_command('compilemessages')
                os.chdir(curr)

            logger.info("handling template")
             # handling the template excepation
            os.chdir("templates")
            # TODO: fix a way for unix platfroms
            os.system ("xcopy /S /Y ..\locale\*.* .\locale")
            call_command('makemessages',all=True)
            os.system ("xcopy /S /Y .\locale\*.* ..\locale")

            logger.info("coming back to curr folder")
            os.chdir(curr)
            call_command('compilemessages')
            '''
        except Exception, e:
            logger.info ( "Exception:  %s" % str( e) )
            raise e
        finally:
             os.chdir(curr)
        return True


tasks.register( findMovieByTitleTask )
tasks.register( findPersonByNameTask )
tasks.register( findShowByIDTask )
tasks.register( fillActorDataTask)
tasks.register( fillShowEpisodesTask )

tasks.register(maintenanceTranslateTask)
tasks.register(maintenanceReIndexTask)