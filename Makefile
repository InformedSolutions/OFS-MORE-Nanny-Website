PROJECT_SETTINGS=django_govuk_app.settings.dev

install:
	pip install -r requirements.txt

test:
	python manage.py test --settings=$(PROJECT_SETTINGS)
	
docker-build:
	docker build -t django-gov-uk-app .

docker-run:
	docker run -d -p 8000:8000 --name django-gov-uk-app -e PROJECT_SETTINGS=$(PROJECT_SETTINGS) django-gov-uk-app

docker-stop:
	docker stop django-gov-uk-app

docker-kill:
	docker rm -f django-gov-uk-app || true

docker-recreate: docker-kill docker-build docker-run