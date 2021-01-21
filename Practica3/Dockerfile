# Dockerfile
FROM python:3.7-alpine

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
        
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development        
        
CMD ["flask", "run"]