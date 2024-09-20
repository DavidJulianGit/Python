dev-start:
	python manage.py runserver --settings=bookstore.settings.dev
dev-startapp:
	cd apps && python ../manage.py startapp $(app) --settings=bookstore.settings.dev
dev-migrate:
	python manage.py migrate --settings=bookstore.settings.dev
dev-makemigrations:
	python manage.py makemigrations --settings=bookstore.settings.dev
dev-shell:
	python manage.py shell --settings=bookstore.settings.dev
dev-shell-plus:
	python manage.py shell_plus --settings=bookstore.settings.dev
dev-install:
	pip install -r requirements/dev.txt
dev-test:
	python manage.py test --settings=bookstore.settings.dev