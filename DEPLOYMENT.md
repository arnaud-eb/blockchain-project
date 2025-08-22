# 🚀 Deployment Guide

## Quick Deploy Options

### 1. Railway (Recommended - Free & Easy)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub account
3. Import your repository
4. Railway will auto-deploy using the `Procfile`
5. Your app will be live at a `railway.app` subdomain

### 2. Render (Free Tier Available)

1. Go to [Render.com](https://render.com)
2. Connect your GitHub repository
3. Choose "Web Service"
4. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn node:app`
   - **Environment**: Python 3

### 3. Heroku (Classic Option)

```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-blockchain-app

# Deploy
git add .
git commit -m "Deploy blockchain app"
git push heroku main

# Open your app
heroku open
```

### 4. Fly.io (Modern Alternative)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Launch app
fly launch
fly deploy
```

## Pre-Deployment Checklist

- [x] `Procfile` configured for Gunicorn
- [x] `requirements.txt` with all dependencies
- [x] `runtime.txt` specifying Python version
- [x] Environment variable support for PORT
- [x] `.gitignore` excluding data files
- [x] `app.json` for Heroku deployment

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 5000 |

## Post-Deployment

1. Visit your live URL
2. Test wallet creation
3. Try mining a block
4. Update README.md with live demo link

## Troubleshooting

### Common Issues

**App won't start**: Check logs for dependency issues
```bash
# Heroku
heroku logs --tail

# Railway
Check logs in Railway dashboard
```

**Mining too slow**: Adjust proof-of-work difficulty in `utility/verification.py`

**CORS errors**: Ensure Flask-CORS is properly configured in `node.py`