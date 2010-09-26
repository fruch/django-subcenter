@echo off

set PATH=%PATH%;C:\Program Files\SlikSvn\bin

echo ----- start VirtualEnv ------------
mkdir .\deploy
virtualenv --no-site-packages --distribute ./deploy
call .\deploy\Scripts\activate.bat

echo ----- Installing dependecies ------
pip install django
pip install pil

easy_install lxml==2.2.2
pip install -e svn+http://django-profile.googlecode.com/svn/trunk/#egg=userprofile
pip install -e svn+http://django-rosetta.googlecode.com/svn/trunk/#egg=rosetta
pip install -e svn+http://django-tagging.googlecode.com/svn/trunk/#egg=tagging
pip install -e git://github.com/muhuk/django-formfieldset.git#egg=formfieldset


pip install south
pip install django-celery
pip install ghettoq

pip install imdbpy
pip install wikitools

rem debugging and testing
pip install django-debug-toolbar
pip install django-unittest-depth
pip install coverage
pip install django_coverage
pip install unittest-xml-reporting

rem compoents that doesn't have setup.py
rem pip install -e svn+http://django-flags.googlecode.com/svn/trunk/#egg=flags
rem pip install -e svn+http://django-transmeta.googlecode.com/svn/trunk/#egg=transmeta

echo -----  Running Tests  ------------
call test.bat

echo -----  deactive VirtualEnv  ------
call .\deploy\Scripts\deactivate.bat