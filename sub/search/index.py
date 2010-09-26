from djapian import space, Indexer, CompositeIndexer

from movies.models import Movie
from persons.models import Actor

class MovieIndexer(Indexer):
    fields = ['summary', 'summary_he']
    tags = [
        ('title', 'title', 3),
        ('title_he', 'title_he', 3),
        ('publish_year', 'publish_year'),
        ('tags', 'tags'),
    ]
    
class ActorIndexer(Indexer):
    fields = ['bio', 'bio_he' ]
    tags = [
        ('name', 'name', 3),
        ('name_he', 'name_he', 3),
        ('tags', 'tags'),
    ]
    

space.add_index(Movie, MovieIndexer, attach_as='indexer')
space.add_index(Actor, ActorIndexer, attach_as='indexer')

complete_indexer = CompositeIndexer(Movie.indexer, Actor.indexer)