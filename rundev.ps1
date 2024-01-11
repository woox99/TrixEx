# PowerShell script
# Execute this script from the django directory: .\rundev.ps1

# Activate the virtual environment (change name of projectname)
TrixExenv/Scripts/activate

# Change to the project directory (change name of projectname)
cd TrixEx

# Run the Django development server
python manage.py runserver



