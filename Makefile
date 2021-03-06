install:
	@[ -f '.env' ] || cp .env.example .env
	@pipenv install -d

build:
	@pipenv lock -r > requirements.txt
	@pipenv lock -d -r > requirements-dev.txt
	@docker-compose build app

up: build
	@docker-compose up -d app

build-cron:
	@pipenv lock -r > requirements.txt
	@pipenv lock -d -r > requirements-dev.txt
	@docker-compose build cronjob

up-cron: build-cron
	@docker-compose up -d cronjob

stop:
	@docker-compose stop

test: build
	@docker-compose run app pytest
	@open ./.tmp/reports/pytest/index.html

migrations: up-data
	@pipenv run python manage.py makemigrations --settings=myproject.settings_myapp

# additional commands

up-data:
	@docker-compose up -d data cache
	@bash ./scripts/wait-data.sh

logs-myapp:
	docker logs -f dp-world-tour_app_1

up-client:
	@docker exec -it dp-world-tour_app_1 python3 manage.py runserver --settings=myproject.settings_client 0.0.0.0:8001

up-mailhost:
	@docker exec -it dp-world-tour_app_1 python -m smtpd -n -c DebuggingServer localhost:1025

clean:
	@docker ps -aq -f status=exited | xargs docker rm
	@docker images -q -f dangling=true | xargs docker rmi
	@find . -name "__pycache__" | xargs rm -rf

clean-data:
	@rm -rf ./.tmp/data

clean-all: clean clean-data

lint: build
	@docker-compose run app pylint myproject myapp
