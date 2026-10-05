FROM python:3.8-slim

WORKDIR /app

COPY hello_flask/app.py .

RUN pip install Flask

EXPOSE 5002

CMD ["python", "app.py"]