FROM python:3.12-alpine

WORKDIR /app

RUN pip install --no-cache-dir redis

COPY main.py .

EXPOSE 3000

CMD ["python", "main.py"]