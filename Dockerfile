########################################################
# BASE
########################################################
FROM python:3.8.0-slim-buster AS base
WORKDIR /app
COPY ./listle /app/listle
COPY ./deploy /app/deploy
RUN pip install -r deploy/requirements.txt


FROM base as local
ENV FLASK_APP=listle
ENV FLASK_ENV=dev
ENV FLASK_DEBUG=True
EXPOSE 5000
CMD flask run --host 0.0.0.0


# ########################################################
# # PROD
# ########################################################
# FROM base as prod
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 notifyless.wsgi:application


########################################################
# TESTER
########################################################
FROM local AS tester
COPY ./setup.cfg /
RUN pip install -r deploy/requirements-test.txt
