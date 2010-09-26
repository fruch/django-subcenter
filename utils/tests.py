"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from utils.tasks import findMovieByTitleTask

class UtilsTest(TestCase):
    def test_FindMovie(self):
        task = findMovieByTitleTask.delay('Stargate')
        self.assertEqual( task.result,  
            {'list': [{'id': '0118480', 'title': u'"Stargate SG-1" (1997)'}, 
            {'id': '0111282', 'title': u'Stargate (1994)'}, 
            {'id': '0374455', 'title': u'"Stargate: Atlantis" (2004)'}, 
            {'id': '0360017', 'title': u'Stargate (1981) (VG)'}, 
            {'id': '0929629', 'title': u'Stargate: Continuum (2008) (V)'}, 
            {'id': '1286039', 'title': u'"SGU Stargate Universe" (2009)'}, 
            {'id': '0942903', 'title': u'Stargate: The Ark of Truth (2008) (V)'}, 
            {'id': '0320969', 'title': u'"Stargate: Infinity" (2002)'}, 
            {'id': '1483803', 'title': u'Stargate SG-1: Children of the Gods - Final Cut (2009) (V)'}, 
            {'id': '0419759', 'title': u'From Stargate to Atlantis: Sci Fi Lowdown (2004) (TV)'}, 
            {'id': '0861734', 'title': u'Sci Fi Inside: Stargate SG-1 200th Episode (2006) (TV)'}, 
            {'id': '0367090', 'title': u'Stargate: The Lowdown (2003) (TV)'}, 
            {'id': '0446593', 'title': u'Sci Fi Lowdown: Behind the Stargate - Secrets Revealed (2005) (TV)'}, 
            {'id': '1080033', 'title': u'Stargate SG-1: True Science (2006) (TV)'}, 
            {'id': '0320391', 'title': u'Stargate SG-3000 (2004)'}, 
            {'id': '0888700', 'title': u'Is There a Stargate? (2003) (V)'}, 
            {'id': '0888706', 'title': u"Making of 'Stargate', The (2003) (V)"}, 
            {'id': '0449102', 'title': u'Stargate Saga, The (1997) (TV)'}, 
            {'id': '1648680', 'title': u'"SGU Stargate Universe Kino" (2009)'}, 
            {'id': '1288405', 'title': u'Stargate: Extinction (2011) (V)'}]} 
        )

    def test_FindShow(self):
        task = findMovieByTitleTask.delay('Stargate', filter="tv series")
        self.assertEqual( task.result,  
        {'list': [{'id': '0118480', 'title': u'"Stargate SG-1" (1997)'}, 
        {'id': '0374455', 'title': u'"Stargate: Atlantis" (2004)'}, 
        {'id': '1286039', 'title': u'"SGU Stargate Universe" (2009)'}, 
        {'id': '0320969', 'title': u'"Stargate: Infinity" (2002)'}, 
        {'id': '1648680', 'title': u'"SGU Stargate Universe Kino" (2009)'}]} )
    
