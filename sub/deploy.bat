@echo off

set PATH=%PATH%;C:\Program Files\SlikSvn\bin

echo ----- start VirtualEnv ------------
mkdir .\deploy
rmdir /S /Q .\deploy\src\

virtualenv --no-site-packages --distribute ./deploy
call .\deploy\Scripts\activate.bat

echo ----- Installing dependecies ------
easy_install lxml==2.2.2
pip install -q -r requirements.pip
pip install -q -r requirements-test.pip
REM pip install django
REM pip install pil

REM pip install -e svn+http://django-profile.googlecode.com/svn/trunk/#egg=userprofile 
REM pip install -e svn+http://django-rosetta.googlecode.com/svn/trunk/#egg=rosetta
REM pip install -e svn+http://django-tagging.googlecode.com/svn/trunk/#egg=tagging
REM pip install -e git://github.com/muhuk/django-formfieldset.git#egg=formfieldset


REM pip install south
REM pip install celery
REM pip install django-celery
REM pip install ghettoq

REM pip install imdbpy
REM pip install wikitools

rem debugging and testing
REM pip install django-debug-toolbar
REM pip install django-unittest-depth
REM pip install coverage
REM pip install django_coverage
REM pip install unittest-xml-reporting
REM pip install pylint
REM pip install -e git://git.chris-lamb.co.uk/django-lint.git#egg=django-lint
rem compoents that doesn't have setup.py
rem pip install -e svn+http://django-flags.googlecode.com/svn/trunk/#egg=flags
rem pip install -e svn+http://django-transmeta.googlecode.com/svn/trunk/#egg=transmeta
echo -----  Patching  ------------
echo 1) patch coverage_runner
xcopy /Y .\common-apps\coverage_runner.py .\deploy\Lib\site-packages\django_coverage\coverage_runner.py
echo 2) make direcorties
mkdir .\public\site_media\userprofile
echo 3) patch imdbpy direcorties
mkdir .\deploy\src\imdbpy
git checkout 4.6
git apply ..\..\..\common-apps\patches\imdbpy\*.*
cd ..\..

echo -----  Running Tests  ------------
call test.bat

echo -----  deactive VirtualEnv  ------
call .\deploy\Scripts\deactivate.bat