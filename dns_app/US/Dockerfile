FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY us_server.py .
EXPOSE 8080
CMD ["python", "-u", "us_server.py"]
