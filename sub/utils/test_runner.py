from django.conf import settings
from django_nose import NoseTestSuiteRunner

class MyTestRunner(NoseTestSuiteRunner):
    def __init__(self, *args, **kwargs):
        settings.CELERY_ALWAYS_EAGER = True
        super(NoseTestSuiteRunner, self).__init__(*args, **kwargs)
