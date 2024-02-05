# PowerShell script
# Execute this script from the django directory: .\createproject.ps1

# Create project directory (change name)
# New-Item -ItemType Directory -Name "TrixEx" -Force 

# cd into new project directroy (change name)
# cd TrixEx

# Create new virtual environment (change name)
python -m venv projectenv

# Activate new virtual environment (change name)
projectenv\scripts\activate

# Install Django
pip install Django

# Create new django project (change name)
django-admin startproject TrixEx

# cd into new project (change name)
cd TrixEx

# Create app (app connot have same name as project)
python manage.py startapp app

# Migrate
python manage.py migrate