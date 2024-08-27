dev-start:
	python3 manage.py runserver --settings=recipe_project.settings.dev
dev-startapp:
	cd apps && python3 ../manage.py startapp $(app) --settings=recipe_project.settings.dev
dev-migrate:
	python3 manage.py migrate --settings=recipe_project.settings.dev
dev-makemigrations:
	python3 manage.py makemigrations --settings=recipe_project.settings.dev
dev-shell:
	python3 manage.py shell --settings=recipe_project.settings.dev
dev-shell-plus:
	python3 manage.py shell_plus --settings=recipe_project.settings.dev
dev-install:
	pip install -r requirements/dev.txt
dev-test:
	python3 manage.py test --settings=recipe_project.settings.dev