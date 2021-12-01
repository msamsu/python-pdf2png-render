WEB_CONT=pdf2png_web
DOCKER_COMPOSE_WEB=docker-compose -p ${WEB_CONT} -f environment/docker-compose.yml

default: up

build:
	${DOCKER_COMPOSE_WEB} build ${DC_OPTS}

up:
	${DOCKER_COMPOSE_WEB} up ${DC_OPTS}

upd:
	${DOCKER_COMPOSE_WEB} up -d ${DC_OPTS}

logs:
	${DOCKER_COMPOSE_WEB} logs -f ${DC_OPTS}

stop:
	docker-compose -f environment/docker-compose.yml stop

rm:
	docker-compose -f environment/docker-compose.yml rm -f

bash:
	${DOCKER_COMPOSE_WEB} exec ${DC_OPTS} ${WEB_CONT} bash

django_command:
	${DOCKER_COMPOSE_WEB} exec ${DC_OPTS} ${WEB_CONT} python manage.py ${COMMAND}

shell_plus:
	${DOCKER_COMPOSE_WEB} exec ${DC_OPTS} ${WEB_CONT} python manage.py shell_plus

test:
	${DOCKER_COMPOSE_WEB} exec ${DC_OPTS} ${WEB_CONT} bash -c "coverage run --source='.' manage.py test ; coverage report"

dbshell:
	${DOCKER_COMPOSE_WEB} exec ${DC_OPTS} ${WEB_CONT} python manage.py dbshell

makemigrations:
	${DOCKER_COMPOSE_WEB} exec ${DC_OPTS} ${WEB_CONT} python manage.py makemigrations

migrate:
	${DOCKER_COMPOSE_WEB} exec ${DC_OPTS} ${WEB_CONT} python manage.py migrate
