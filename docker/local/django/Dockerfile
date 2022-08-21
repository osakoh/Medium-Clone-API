# ARG: variable to build a Docker image
ARG PYTHON_VERSION=3.9-slim-bullseye

FROM python:${PYTHON_VERSION} as python

FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
   build-essential \
   libpq-dev


COPY ./requirements .

# wheels: faster installation & stability
RUN pip wheel --wheel-dir /usr/src/app/wheels \
   -r ${BUILD_ENVIRONMENT}.txt


FROM python as python-run-stage
ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

# prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# python output is displayed in the terminal without being buffered
ENV PYTHONUNBUFFERED 1

ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# system dependency
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


# copy python deps from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/
# use wheels to install python deps
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
   && rm -rf /wheels/

# db service available before starting the api service
# sed: convert windows line-ending to unix line-ending using sed
# Windows: CR LF; Unix: LF; Macintosh: CR
COPY ./docker/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
# grant execution rights
RUN chmod +x /entrypoint


# migrate models, runserver, & collect static files
# sed: convert windows line-ending to unix line-ending using sed
# Windows: CR LF; Unix: LF; Macintosh: CR
COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start
# grant execution rights
RUN chmod +x /start


# sed: convert windows line-ending to unix line-ending using sed
# Windows: CR LF; Unix: LF; Macintosh: CR
COPY ./docker/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
# grant execution rights
RUN chmod +x /start-celeryworker


# sed: convert windows line-ending to unix line-ending using sed
# Windows: CR LF; Unix: LF; Macintosh: CR
COPY ./docker/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
# grant execution rights
RUN chmod +x /start-flower

# copy application code to working directory
COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint"]