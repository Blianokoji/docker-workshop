FROM python:3.12-alpine

WORKDIR /app

# Create the data directory
RUN mkdir -p /app/data

# Copy single-file app
COPY app.py .

# Document volume target and port
VOLUME /app/data
EXPOSE 5000

CMD ["python", "app.py"]