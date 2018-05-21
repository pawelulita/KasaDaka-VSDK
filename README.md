# KasaDaka-Voice Service Development Kit

## Installation instructions

Download the Python 3.6.5 distribution and install it.
Ensure you have a git client installed, and clone the repository in a directory.
Open a shell in that directory and run the commands:

```
> python manage.py collectstatic
> python manage.py makemigrations polls
> python manage.py makemigrations nums
> python manage.py makemigrations service_development
> python manage.py migrate
> python manage.py createsuperuser
> python manage.py loaddata db_data_backup.json
> python manage.py runserver
```

For `createsuperuser`: enter a username, email and password.
