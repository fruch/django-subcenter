# -*- coding: utf-8 -*-

from django.test import TestCase
from shows.models import Show, Season, Episode
from django.core.urlresolvers import reverse
import json
    
class PersonsTests(TestCase):
    
    def setUp(self):
        from django.contrib.auth.models import User
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.is_staff = True
        user.save()
        r = self.client.login(username='john', password='johnpassword')
        self.assertEqual(r, True)
    
    def test_edb_translation(self): 
    
        r = self.client.get("/actors/edb_translate_name/json/Benny%20Gantz/", {} ,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(r.content)['he_name'], u'בני גנץ')
    
        r = self.client.get("/actors/edb_translate_name/json/Stellan%20Skarsg%C3%A5rd/", {} ,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(r.content)['he_name'], u'סטלאן סקארסגארד')
    
        #no found translation
        r = self.client.get("/actors/edb_translate_name/json/Yoav%20Donat/", {} ,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual( r.content, u'{"error": true}') 
    
    def test_Find_in_imdb(self):
        r = self.client.get("/actors/imdb_get_info/json/1745/", {} ,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        t = json.loads( r.content )
    
        self.assertEqual( t['birth_date'], u'13 June 1951')
        self.assertEqual( t['imdb_url'], u'http://www.imdb.com/name/nm1745/')
        self.assertEqual( t['name'], u'Stellan Skarsg\xe5rd')
    

