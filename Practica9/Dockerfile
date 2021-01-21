FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /app_9
COPY . /app_9/
# COPY requirements.txt /app_9/

RUN pip install -r requirements.txt

CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8000", "--chdir", "app_9", "mi_sitio_web.wsgi:application"]