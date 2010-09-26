mkdir ./deploy
virtualenv --no-site-packages --distribute ./deploy
cmd.exe /c .\\deploy\\Scripts\\activate.bat
pip install django