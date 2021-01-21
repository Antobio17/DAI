all:
	docker-compose up
build:
	docker-compose build
migrate:
	docker-compose run app python manage.py migrate
makemigrations:
	docker-compose run app python manage.py makemigrations

