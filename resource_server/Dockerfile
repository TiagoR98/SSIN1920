FROM python:alpine

# Update package repositories information
RUN apk update
RUN apk upgrade

# Install libpq
RUN apk add --update --upgrade git gcc musl-dev libjpeg-turbo-dev zlib-dev postgresql-dev

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "manage.py", "runserver"]
