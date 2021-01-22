all:
	docker-compose up
build:
	docker-compose build
migrate:
	docker-compose run app_10 python manage.py migrate
makemigrations:
	docker-compose run app_10 python manage.py makemigrations

