import solango
from movies.models import Movie

class MovieDocument(solango.SearchDocument):
    date = solango.fields.DateField()
    title = solango.fields.CharField(copy=True)
    content = solango.fields.TextField(copy=True)

    def transform_date(self, instance):
        return instance.created

    def transform_content(self, instance):
        return instance.summary

solango.register(Movie, MovieDocument)