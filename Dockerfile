FROM python:3.8-slim

# Add a user (change as needed)
# Prevents running sudo commands
RUN useradd -r -s /bin/bash scrape-app

# Install dependencies and browsers
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    wget \
    curl \
    gnupg \
    ca-certificates \
    firefox-esr \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxrender1 \
    xdg-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Install Edge
RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add - \
    && wget -q https://packages.microsoft.com/config/debian/10/prod.list -O /etc/apt/sources.list.d/microsoft-edge.list \
    && apt-get update \
    && apt-get install -y microsoft-edge-stable

# Download and set up ChromeDriver
RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -q "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip \
    && rm chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/chromedriver

# Download and set up geckodriver for Firefox
RUN GECKODRIVER_VERSION=$(curl -sS https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d\" -f4) \
    && wget -q "https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz" \
    && tar -xzf geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz \
    && rm geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/geckodriver

# Download and set up EdgeDriver
RUN EDGE_DRIVER_VERSION=$(curl -sS https://msedgedriver.azureedge.net/LATEST_RELEASE) \
    && wget -q "https://msedgedriver.azureedge.net/${EDGE_DRIVER_VERSION}/edgedriver_linux64.zip" \
    && unzip edgedriver_linux64.zip \
    && rm edgedriver_linux64.zip \
    && mv msedgedriver /usr/local/bin/msedgedriver

# Set current environment
ENV HOME /app
WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Switch to user app to avoid excessive permissions
RUN chown -R scrape-app:scrape-app /app
USER scrape-app

# Install Python dependencies
ADD ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt --user

# Add the rest of the files
COPY . /app

# Expose all ports
EXPOSE 5000

# Command to start Flask server
CMD ["flask", "run", "--host=0.0.0.0"]
