web: (
    python manage.py makemigrations api core && 
    python manage.py migrate && 
    gunicorn mysite.wsgi
)