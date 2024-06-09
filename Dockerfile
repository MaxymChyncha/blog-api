FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN mkdir -p /app/files/media/

RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user

RUN chown -R my_user /app/files/media
RUN chmod -R 755 /app/files/media

USER my_user
