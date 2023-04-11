FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install pipenv

WORKDIR /app

COPY Pipfile /app/
COPY Pipfile.lock /app/

RUN pipenv install --system --deploy

COPY . /app/

CMD ["python", "manage.py", "runserver",]