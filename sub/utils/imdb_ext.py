from imdb import IMDb
import log
logger = log.get_logger()

def do_long_imdb_operation(func, args=None,MAX_RETRY=3, timeout=10):
    
    import socket 
    from imdb._exceptions import IMDbDataAccessError
    socket.setdefaulttimeout(timeout)
    
    ret = None
    fetch = True
    retries = 0
    while fetch:
        if retries >= MAX_RETRY: break
        try:
            
            retries += 1
            logger.warn("try #%d" % retries)
            if args == None:
                ret = func()
            else:
                ret = func(args)
            
            fetch = False
        except socket.timeout: logger.warn("timeout") 
        except IOError: logger.warn("timeout") 
        except IMDbDataAccessError:logger.warn("timeout") 
    
    socket.setdefaulttimeout(None)
    return ret, not fetch
    
def search_movie_by_title(title):
    ia = IMDb('http')
    movies = ia.search_movie(title)
    return movies
    
def getmovie_by_id(id):    
    ia = IMDb('http')
    movie = ia.get_movie(id)
    return movie
    
def update_episodes(movie):
    ia = IMDb('http')
    ia.update(movie, 'episodes')
    return movie

def search_person_by_name(name):
    ia = IMDb('httpThin')
    actors = ia.search_person(name)
    return actors

def getperson_by_id(person_id):
    ia = IMDb('http')
    person = ia.get_person(person_id)
    return person