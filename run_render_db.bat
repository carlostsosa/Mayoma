@echo off
set DB_ENGINE=django.db.backends.postgresql
set DB_NAME=mayoma_db
set DB_USER=mayoma_db_user
set DB_PASSWORD=xDJdBBuPBhBql4SwagUjlzk22Mwkq42k
set DB_HOST=dpg-d9kbl3vavr4c73al3570-a.oregon-postgres.render.com
set DB_PORT=5432
set DISABLE_AUTH=True
cd /d C:\Softanel\Documentos\GitHub\Mayoma
python manage.py runserver 0.0.0.0:8000 --noreload
