# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from movies.models import Movie
import json

class MoviesTests(TestCase):
    def setUp(self):
        """ seting up the env for the test """
        from django.contrib.auth.models import User
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.is_staff = True
        user.save()
        r = self.client.login(username='john', password='johnpassword')
        
        self.assertEqual(r, True)
        
    def test_empty_movie_list(self):
        r = self.client.get('/movies/', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context['object_list']), u'[]')
    
    def test_adding_movie(self):
        movie = Movie(title_en='Terminator ver 1', title_he=u'טרמינטור אחד' )
        movie.imdb_rating = str(9.5)
        movie.save()
        
        self.assertEqual(unicode(movie.title_he), u'טרמינטור אחד')
    
        r = self.client.get(movie.get_absolute_url(), {})
        self.assertEqual(r.status_code, 200)
        obj = r.context['object']
        self.assertEqual(obj.title, u'Terminator ver 1')  
        self.assertEqual(obj.title_he, u'טרמינטור אחד')    
        self.assertEqual(obj.slug, u'terminator-ver-1')   
        self.assertEqual(float(obj.imdb_rating), 9.5 )
        
    def test_ajax_get_movie_list(self):
        r = self.client.get(reverse('movie_imdb_search_by_title', args=['json','stargate']) , {} ,HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content, 
            '{"list": [{"id": "0111282", "title": "Stargate (1994)"}, {"id": "0320391", "title": "Stargate SG-3000 (2004)"}]}')

    def test_ajax_get_movie_by_id(self):
        r = self.client.get(reverse('movie_imdb_get_info', args=['json','0111282']) , {} ,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.assertEqual(j['genre'],'["Fantasy", "Action", "Adventure", "Sci-Fi"]') 
        self.assertEqual(j['year'], 1994)
        self.assertEqual(j['title'],u'Stargate')