FROM python:3.8-slim

# Add a user (change as needed)
# Prevents running sudo commands
RUN useradd -r -s /bin/bash scrape-app
RUN apt-get update && apt-get install -y gcc python3-dev

# Set current environment
ENV HOME /app
WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Switch to user app to avoid excessive permissions
RUN chown -R scrape-app:scrape-app /app
USER scrape-app

# Install dependencies
ADD ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt --user

# Add the rest of the files
COPY . /app

# Expose all ports
EXPOSE 5000

# Command to start Flask server
CMD ["flask", "run", "--host=0.0.0.0"]
