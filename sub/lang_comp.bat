@echo off
set OLD_PATH=%PATH%
set PATH=%PATH%;%CD%\ext_utils\xgettext\bin

cd movies 
python ..\manage.py makemessages -a
python ..\manage.py compilemessages
cd ..

cd shows
python ..\manage.py makemessages -a
python ..\manage.py compilemessages
cd ..

cd persons 
python ..\manage.py makemessages -a
python ..\manage.py compilemessages
cd ..

cd profiles 
python ..\manage.py makemessages -a
python ..\manage.py compilemessages
cd..

cd templates 
xcopy /S /Y ..\locale\*.* .\locale
python ..\manage.py makemessages -a
xcopy /S /Y ..\locale\*.* .\locale
cd ..
python manage.py compilemessages

set PATH=%OLD_PATH%