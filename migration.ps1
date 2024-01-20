# PowerShell script
# Execute this script from django directorey

# This will create a table in your SQLite db with the name of the class in your app -> models.py
# Class in models.py must be created BEFORE this
# "app" must be in settings
# project urls.py must be directed to app -> urls.py

# Mirgration must be done EVERY time model is changed (change directory name)
# cd TrixEx
cd TrixEx
python manage.py makemigrations
python manage.py migrate



