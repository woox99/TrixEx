# PowerShell script
# Execute this script from the django directory: .\createproject.ps1

# Create new virtual environment (change name)
python -m venv TrixExenv

# Activate new virtual environment (change name)
TrixExenv\scripts\activate

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