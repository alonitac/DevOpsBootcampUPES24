FROM python:3.11-slim
WORKDIR /app
RUN pip install Flask prometheus-client requests

COPY app.py /app/app.py
EXPOSE 8081
CMD ["python3", "app.py"]
