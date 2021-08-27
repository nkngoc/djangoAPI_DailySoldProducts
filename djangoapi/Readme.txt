run venv\Script\Activate
run python manage.py migrate
run python manage.py runserver
run python manage.py startapp rest_api
run python manage.py runserver
s-3
step 1: python manage.py makemigrations
step 2: python manage.py migrate
step 3: python manage.py startapp rest_api
step 4: python manage.py migrate
step 5: python manage.py createsuperuser
s-3
step 6: python manage.py runserver