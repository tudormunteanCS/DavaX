FROM python:3.13-slim AS backend-builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR ./app

COPY ./requirements.txt ./

RUN pip install --upgrade pip \
 && pip install -r requirements.txt



FROM python:3.13-slim


WORKDIR ./app
COPY --from=backend-builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin
COPY . .

RUN mkdir -p db && touch db/identifier.sqlite


EXPOSE 5050
#ENV FLASK_APP=algo:create_app
CMD ["gunicorn", "-b", "0.0.0.0:5050", "algo:app"]