# Azure Deployment Guide

This guide covers deploying the Django application to **Azure App Service** and **Azure Container Apps**.

## Prerequisites

1. **Production Server**: Install `gunicorn` (recommended for production).
   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```
2. **Settings**:
   - In `azure_project/settings.py`, set `DEBUG = False`.
   - Update `ALLOWED_HOSTS` with your production domain (e.g., `['myapp.azurewebsites.net']`).

---

## Option 1: Azure App Service (Code)

Deploy directly from your local Git repository or VS Code to Azure App Service (Linux).

### Configuration
1. **Startup Command**:
   Configure the startup command in the Azure Portal > **Configuration** > **General Settings** > **Startup Command**:
   ```bash
   gunicorn --bind=0.0.0.0 --timeout 600 azure_project.wsgi
   ```

2. **Environment Variables**:
   Set `App Settings` in the Azure Portal for your database credentials (as defined in `settings.py` via `os.environ` if you updated it to use env vars, or ensure `settings.py` has the correct values).

### Deployment Steps
1. **VS Code**: Use the "Azure Tools" extension to "Deploy to Web App...".
2. **CLI**:
   ```bash
   az webapp up --runtime "PYTHON:3.11" --sku B1 --logs
   ```

---

## Option 2: Azure Container Apps / App Service (Container)

Deploy using a Docker container. This is recommended for consistency and if you need specific system dependencies.

### 1. Create a `Dockerfile`
Create a file named `Dockerfile` in the project root:

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (needed for ODBC driver)
RUN apt-get update && apt-get install -y \
    curl gnupg2 apt-transport-https unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose port and run server
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "azure_project.wsgi"]
```

### 2. Build and Push to Azure Container Registry (ACR)
```bash
az acr build --registry <your-registry-name> --image django-app:latest .
```

### 3. Deploy
- **App Service**: Create a Web App for Containers and select the image from your ACR.
- **Container Apps**: Create a Container App and select the image from your ACR.
  - Target Port: `8000`
  - Ingress: Enabled (External)
