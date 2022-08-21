build:
	docker compose -f local.yml up --build --remove-orphans

up:
	docker compose -f local.yml up

down:
	docker compose -f local.yml down

bash:
	docker compose -f local.yml exec -it api ./docker/local/django/entrypoint bash


view-logs:
	docker compose -f local.yml logs


migrate:
	docker compose -f local.yml run --rm api python3 manage.py migrate


makemigrations:
	docker compose -f local.yml run --rm api python3 manage.py makemigrations


collectstatic:
		docker compose -f local.yml run --rm api python3 manage.py collectstatic --noinput --clear


superuser:
		docker compose -f local.yml run --rm api python3 manage.py createsuperuser


down-v:
		docker compose -f local.yml down -v


volumes:
	docker volume inspect blogapi_local_postgres_data


blog-db:
	docker compose -f local.yml exec postgres psql --username=dbUser --dbname=blog-api


flake8:
	docker compose -f local.yml exec api flake8 .

black-check:
	docker compose -f local.yml exec api black --check --exclude=migrations .

black-diff:
	docker compose -f local.yml exec api black --diff --exclude=migrations .

black:
	docker compose -f local.yml exec api black --exclude=migrations .

isort-check:
	docker compose -f local.yml exec api isort . --check-only --skip venv --skip migrations

isort-diff:
	docker compose -f local.yml exec api isort . --diff --skip venv --skip migrations

isort:
	docker compose -f local.yml exec api isort . --skip venv --skip migrations

config:
	docker compose -f local.yml config

restart-api:
	docker compose -f local.yml restart api

restart-all:
	docker compose -f local.yml restart

flush:
	docker compose -f local.yml run --rm api python3 manage.py flush --noinput

rebuild-index:
	docker compose -f local.yml run --rm api python3 manage.py rebuild_index --noinput

postgres:
	docker compose -f local.yml exec -it postgres bash

nginx:
	docker compose -f local.yml exec -it nginx bash

backup:
	docker compose -f local.yml exec postgres backup

backups:
	docker compose -f local.yml exec postgres backups

%:
	@:

# $(MAKECMDGOALS) is the list of "targets" i.e. restore
# filter-out is a function that removes some elements from a list
#$(filter-out $@,$(MAKECMDGOALS)) returns the list of targets specified on the command line other than "restore", which in this case is the name of the postgres backup file
args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

restore:
	docker compose -f local.yml exec postgres restore $(call args,defaultstring)

#delete:
#	#docker compose kill $(docker ps -q)
#	docker rm $(call args, docker ps -a -q)
#	docker rmi $(docker images -q)
#	docker system prune -f
#	docker volume prune -f