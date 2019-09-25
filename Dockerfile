FROM python:alpine

WORKDIR /app

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /app/Pipfile
RUN pipenv install --skip-lock --system --dev

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
