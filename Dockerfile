FROM python:3.10-alpine

WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install the dependencies
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

# Copy the application code
COPY . .

# Expose the port
EXPOSE 80

# Start the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
