# Deployment Guide for Instana APM Dashboard

This guide provides step-by-step instructions for deploying the Instana APM Synthetic Data Dashboard to production platforms.

## Prerequisites

- GitHub repository with all code committed
- Heroku CLI installed (or Azure CLI for Azure deployment)
- Python 3.10+ environment
- All dependencies listed in `requirements.txt`

## Option 1: Deploy to Heroku

### Step 1: Prepare the Application

1. Ensure `Procfile` exists with correct content:
   ```
   web: gunicorn dashboard:app.server
   ```

2. Ensure `requirements.txt` includes all dependencies:
   ```
   dash
   pandas
   plotly
   gunicorn
   requests
   slack_sdk
   dash-auth
   ```

3. Ensure `runtime.txt` specifies Python version:
   ```
   python-3.10.12
   ```

### Step 2: Create Heroku App

```bash
# Login to Heroku
heroku login

# Create new app
heroku create instana-apm-dashboard

# Set environment variables
heroku config:set DASH_USERNAME=admin
heroku config:set DASH_PASSWORD=your_secure_password
heroku config:set SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
```

### Step 3: Deploy

```bash
# Add Heroku remote
heroku git:remote -a instana-apm-dashboard

# Push to Heroku
git push heroku main

# Scale the app
heroku ps:scale web=1

# Open the app
heroku open
```

### Step 4: Configure Data Generation

Set up automated data generation:

```bash
# Add scheduler addon
heroku addons:create scheduler:standard

# Schedule data generation (runs every hour)
heroku scheduler:add "python scripts/generate_instana_all.py --seed 42 --entities 120 --apps 15 --services 40 --issues 30" --frequency "hourly"
```

## Option 2: Deploy to Azure App Service

### Step 1: Prepare Azure Resources

```bash
# Login to Azure
az login

# Create resource group
az group create --name instana-dashboard-rg --location eastus

# Create App Service plan
az appservice plan create --name instana-plan --resource-group instana-dashboard-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group instana-dashboard-rg --plan instana-plan --name instana-apm-dashboard --runtime "PYTHON:3.10"
```

### Step 2: Configure Environment

```bash
# Set environment variables
az webapp config appsettings set --name instana-apm-dashboard --resource-group instana-dashboard-rg --setting DASH_AUTH_USERNAME=admin
az webapp config appsettings set --name instana-apm-dashboard --resource-group instana-dashboard-rg --setting DASH_AUTH_PASSWORD=your_secure_password
```

### Step 3: Deploy

```bash
# Deploy via Git
az webapp deployment source config --name instana-apm-dashboard --resource-group instana-dashboard-rg --repo-url https://github.com/yourusername/your-repo --branch main --manual-integration
```

## Option 3: Deploy to AWS Elastic Beanstalk

### Step 1: Install EB CLI

```bash
pip install awsebcli
```

### Step 2: Initialize EB Application

```bash
# Initialize
eb init -p python-3.10 instana-apm-dashboard

# Create environment
eb create instana-dashboard-env
```

### Step 3: Configure Environment Variables

Create `.ebextensions/environment.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    DASH_AUTH_USERNAME: admin
    DASH_AUTH_PASSWORD: your_secure_password
    SLACK_WEBHOOK_URL: https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
```

### Step 4: Deploy

```bash
eb deploy
```

## Production Configuration

### Environment Variables

Set these environment variables in your deployment platform:

```bash
DASH_AUTH_USERNAME=admin
DASH_AUTH_PASSWORD=your_secure_password
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
DATA_REFRESH_INTERVAL=3600  # seconds
```

### Data Persistence

For production data persistence:

1. **Database Option**: Modify dashboard to use PostgreSQL/MySQL instead of JSONL files
2. **File Storage**: Use cloud storage (AWS S3, Azure Blob Storage) for data files
3. **Scheduled Jobs**: Set up cron jobs or cloud schedulers for data generation

### Monitoring & Alerting

1. **Application Monitoring**: Use platform built-in monitoring (Heroku metrics, Azure Application Insights)
2. **Custom Alerts**: Configure alerts for dashboard downtime
3. **Log Aggregation**: Set up log shipping to services like Papertrail or Azure Log Analytics

## Security Considerations

1. **Authentication**: Change default credentials
2. **HTTPS**: Ensure SSL/TLS is enabled
3. **Network Security**: Configure firewalls and access controls
4. **Data Encryption**: Encrypt sensitive configuration data

## Scaling Considerations

1. **Horizontal Scaling**: Configure load balancer for multiple instances
2. **Database Scaling**: Use managed database services for data persistence
3. **Caching**: Implement Redis for data caching
4. **CDN**: Use CDN for static assets

## Troubleshooting

### Common Issues

1. **Module Import Errors**: Ensure all dependencies are in `requirements.txt`
2. **Data Loading Errors**: Verify data file paths and permissions
3. **Memory Issues**: Increase instance size for large datasets
4. **Timeout Issues**: Configure longer timeouts for data processing

### Logs

Check application logs:
```bash
# Heroku
heroku logs --tail

# Azure
az webapp log download --name instana-apm-dashboard --resource-group instana-dashboard-rg

# AWS
eb logs
```

## Post-Deployment Checklist

- [ ] Dashboard loads successfully
- [ ] All tabs display data correctly
- [ ] Authentication works
- [ ] Data refreshes automatically
- [ ] Alerts are sent (if configured)
- [ ] SSL certificate is valid
- [ ] Performance is acceptable (< 5s load time)
- [ ] Mobile responsive design works

## Cost Optimization

- **Heroku**: Use Hobby/Basic dynos for development, Standard/Performance for production
- **Azure**: Use Basic/App Service plans for small deployments
- **AWS**: Use t2.micro for development, larger instances for production

## Next Steps

1. Set up monitoring for the dashboard itself
2. Configure automated backups
3. Set up CI/CD pipeline for future deployments
4. Document user access and sharing procedures
