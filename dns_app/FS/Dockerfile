FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY fs_server.py .
EXPOSE 9090
CMD ["python", "-u", "fs_server.py"]
