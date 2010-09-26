# -*- coding: utf-8 -*-

from django.test import TestCase
from shows.models import Show, Season, Episode
from django.core.urlresolvers import reverse

class ShowsTests(TestCase):

    def setUp(self):
        from django.contrib.auth.models import User
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.is_staff = True
        user.save()
        r = self.client.login(username='john', password='johnpassword')
        self.assertEqual(r, True)
           
    def test_01_Shows_list(self):
         r = self.client.get(reverse("show_imdb_search_by_title", args=['json', 'Stargate']), 
                            {} ,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
         self.assertEqual(r.status_code, 200)
             
         
    def test_02_Adding_Shows(self):
    
        r = self.client.post( reverse("show_add"), {'title_he': 'סטארגייט: יקום', 'tags': '', 'poster': '', 'imdb_poster': 'http://ia.media-imdb.com/images/M/MV5BOTEzNTY5NDY5M15BMl5BanBnXkFtZTcwMTY4MDQ3Mg@@._V1._SX95_SY140_.jpg', 'title_en': 'SGU Stargate Universe', 'years': '2009-', 'cast': '[{"id": "0001015", "name": "Robert Carlyle"}, {"id": "0521878", "name": "Justin Louis"}, {"id": "1668284", "name": "Brian J. Smith"}, {"id": "1137028", "name": "Elyse Levesque"}, {"id": "2437382", "name": "David Blue"}, {"id": "0435509", "name": "Alaina Huffman"}, {"id": "0808607", "name": "Jamil Walker Smith"}]', 'imdb_rating': '', 'summary_en': 'The Previously unknown purpose of the "Ninth Cheveron" is revealed, and ends up taking a team to an Ancient ship "Destiny", a ship built millions of years ago by the Ancients, used to seed Distant galaxies with Stargates. This team, led by Dr. David Rush and Colonel Everet Young, are trapped on the ship, unable to change its programmed mission, and encounter new races, new technology and new enemies, as the runaway ship takes them to the far ends of the Universe.::Jwhitleymail', 'summary_he': '', 'csrfmiddlewaretoken': '5c8c31a502fdc4a6b0f9c9c136f942bc', 'imdb_id': '1286039', 'genre': '["Action", "Adventure", "Sci-Fi"]', })
        self.assertEqual(r.status_code, 302 )
        
        r = self.client.get( reverse("fill_show_episodes", args=['json', 'SGU Stargate Universe']) , {} ,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200 )
        
        r = self.client.get( reverse('episode_item', args=['sgu-stargate-universe','01' , '01-air-part-1']) )
        self.assertEqual(r.status_code, 200 )
        
    def test_03_View_Failure(self): 
        
        r = self.client.get(reverse('season_item', args=['stargat','02']) )
        self.assertEqual( r.status_code, 404 )
        
        r = self.client.get( reverse('episode_item', args=['stargate-sg-1','05' , '03-prisoners']) )
        self.assertEqual( r.status_code, 404 )
        
    def test_04_Adding_show_seasons_episodes(self):
        show, created = Show.objects.get_or_create(title_en='Stargate SG-1' , imdb_id=118480 )
               
        season , created = Season.objects.get_or_create( season_num=1,part_of=show)
        
        self.assertEqual(season.get_absolute_url(), '/shows/stargate-sg-1/s01/')
        
        episode , created = Episode.objects.get_or_create(title_en='Sleepless', episode_num=1,part_of=season)
        
        self.assertEqual(episode.get_absolute_url(), '/shows/stargate-sg-1/s01/e01-sleepless/')
        
        r = self.client.get( reverse("fill_show_episodes", args=['json', 'Stargate%20SG-1']) 
                            , {} ,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200 )
        
        seasons = show.seasons.all()
        self.assertEqual( str(seasons[0]) , 'Stargate SG-1 S1' )
        self.assertEqual( str(seasons[1]) , 'Stargate SG-1 S2' )
        
        r = self.client.get( reverse('season_item', args=['stargate-sg-1','02']) )
        self.assertEqual( str(r.context['object']), 'Stargate SG-1 S2')
        
        r = self.client.get( reverse('episode_item', args=['stargate-sg-1','02' , '19-one-false-step']) ) 
        self.assertEqual( str(r.context['object']),'Stargate SG-1 S2E19 "One False Step"')
        
