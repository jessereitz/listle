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
FROM base as prod
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 "listle:create_app()"


########################################################
# TESTER
########################################################
FROM local AS tester
COPY ./setup.cfg /
COPY ./tests /app/tests
RUN pip install -r deploy/requirements-test.txt
