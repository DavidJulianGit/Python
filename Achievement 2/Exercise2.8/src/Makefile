dev-start:
	python manage.py runserver --settings=recipe_project.settings.dev
dev-startapp:
	cd apps && python ../manage.py startapp $(app) --settings=recipe_project.settings.dev
dev-migrate:
	python manage.py migrate --settings=recipe_project.settings.dev
dev-makemigrations:
	python manage.py makemigrations --settings=recipe_project.settings.dev
dev-shell:
	python manage.py shell --settings=recipe_project.settings.dev
dev-shell-plus:
	python manage.py shell_plus --settings=recipe_project.settings.dev
dev-install:
	pip install -r requirements/dev.txt
dev-test:
	python manage.py test --settings=recipe_project.settings.dev --verbosity=2
dev-check:
	python manage.py check --deploy --settings=recipe_project.settings.dev

# Production
prod-start:
	python manage.py runserver --settings=recipe_project.settings.prod
prod-install:
	pip install -r requirements/prod.txt
prod-migrate:
	python manage.py migrate --settings=recipe_project.settings.prod

prod-mm:
	python manage.py makemigrations --settings=recipe_project.settings.prod
prod-superuser:
	python manage.py createsuperuser --settings=recipe_project.settings.prod
prod-gunicorn:
	gunicorn --env DJANGO_SETTINGS_MODULE=recipe_project.settings.prod --bind 0.0.0.0:8000 -c recipe_project/prod/prod.py --log-file -
prod-collectstatic:
	python manage.py collectstatic --settings=recipe_project.settings.prod


# Export Project Structure
struct:
	tree /F /A > structure.txt