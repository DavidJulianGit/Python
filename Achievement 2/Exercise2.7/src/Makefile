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
