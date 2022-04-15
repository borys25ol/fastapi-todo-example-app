# Pull official base image
FROM python:3.10.4-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install packages for virtual envitonment
RUN apt-get update -y \
    && apt -y update && apt -y upgrade \
    && apt-get install -y build-essential \
    && apt-get install -y python3-virtualenv \
    && apt-get install -y netcat \
    && apt-get autoremove -y \
    && apt-get autoclean -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3.10 -m venv /ve

# Enable venv
ENV PATH="/ve/bin:$PATH"

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --upgrade -r /app/requirements.txt

# Copy project
COPY . /app

# Add entrypoint file
COPY /docker/init_app.sh /
RUN chmod +x /init_app.sh

ENTRYPOINT ["/init_app.sh"]
