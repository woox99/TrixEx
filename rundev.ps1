# PowerShell script
# Execute this script from the django directory: .\rundev.ps1

# cd into project folder
# cd 80_Validation

# Activate the virtual environment (change name of projectname)
projectenv/Scripts/activate

# Change to the project directory (change name of projectname)
cd TrixEx

# Run the Django development server
python manage.py runserver



