# Deployment Guide: Whatnot Price Checker

## 🚀 Replit.com Deployment (Recommended)

### Step 1: Create New Repl

1. Go to [Replit.com](https://replit.com)
2. Click "Create Repl"
3. Select "Python" as the template
4. Name your repl: "whatnot-price-checker"
5. Click "Create Repl"

### Step 2: Upload Project Files

**Method A: Drag and Drop**
1. Download the entire `whatnot-price-checker` folder
2. Drag the folder into the Replit file explorer
3. Wait for upload to complete

**Method B: Manual Upload**
1. Create the following folder structure in Replit:
   ```
   whatnot-price-checker/
   ├── src/
   │   ├── static/
   │   │   └── index.html
   │   ├── routes/
   │   │   ├── __init__.py
   │   │   ├── user.py
   │   │   ├── price_checker.py
   │   │   └── advanced_calculator.py
   │   ├── models/
   │   │   ├── __init__.py
   │   │   └── user.py
   │   ├── database/
   │   └── main.py
   ├── venv/
   ├── requirements.txt
   ├── README.md
   └── performance_test.py
   ```

2. Copy and paste the content of each file from the provided code

### Step 3: Configure Replit

1. **Set the run command**:
   - Click on the "Shell" tab
   - Type: `cd whatnot-price-checker && python src/main.py`
   - Or set in `.replit` file:
     ```toml
     run = "cd whatnot-price-checker && python src/main.py"
     ```

2. **Install dependencies**:
   - In the Shell tab, run:
     ```bash
     cd whatnot-price-checker
     pip install -r requirements.txt
     ```

### Step 4: Environment Setup

1. **Create `.env` file** (optional):
   ```env
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   ```

2. **Configure secrets** (if needed):
   - Click on "Secrets" tab in Replit
   - Add any API keys or sensitive configuration

### Step 5: Deploy

1. **Click the "Run" button** in Replit
2. **Wait for startup** - you should see:
   ```
   * Running on all addresses (0.0.0.0)
   * Running on http://0.0.0.0:5000
   ```
3. **Access your app** - Replit will provide a public URL
4. **Test the functionality** with a sample product

### Step 6: Make it Always-On (Optional)

For 24/7 availability:
1. Upgrade to Replit Hacker plan
2. Enable "Always On" for your repl
3. Your app will stay live even when you close the browser

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "src/main.py"]
```

### Build and Run
```bash
docker build -t whatnot-price-checker .
docker run -p 5000:5000 whatnot-price-checker
```

## ☁️ Cloud Platform Deployment

### Heroku
1. Create `Procfile`:
   ```
   web: python src/main.py
   ```
2. Deploy:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   heroku create whatnot-price-checker
   git push heroku main
   ```

### Railway
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python src/main.py`

### Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
   ```json
   {
     "builds": [
       {
         "src": "src/main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "src/main.py"
       }
     ]
   }
   ```
3. Deploy: `vercel --prod`

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Setup Steps
1. **Extract the project**:
   ```bash
   cd whatnot-price-checker
   ```

2. **Create virtual environment** (if not included):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python src/main.py
   ```

5. **Access locally**:
   ```
   http://localhost:5000
   ```

## 🌐 Production Considerations

### Security
- Change the default `SECRET_KEY` in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement rate limiting for API endpoints

### Performance
- Use a production WSGI server (Gunicorn, uWSGI)
- Enable caching for frequently requested products
- Implement connection pooling for external APIs
- Use a CDN for static assets

### Monitoring
- Set up health check endpoints
- Monitor response times and error rates
- Log API usage and performance metrics
- Set up alerts for downtime

## 🚨 Troubleshooting

### Common Deployment Issues

**"Module not found" errors**:
```bash
pip install -r requirements.txt
```

**Port binding issues**:
- Ensure the app binds to `0.0.0.0:5000`
- Check if port 5000 is available
- Try a different port if needed

**Static files not loading**:
- Verify the static folder path in Flask config
- Check file permissions
- Ensure files are uploaded correctly

**API timeouts**:
- Check internet connectivity
- Verify external API endpoints are accessible
- Increase timeout values if needed

### Performance Issues

**Slow response times**:
- Check server location vs. user location
- Optimize API calls and caching
- Monitor server resources (CPU, memory)

**High memory usage**:
- Implement connection pooling
- Clear unused variables
- Monitor for memory leaks

## 📊 Monitoring and Analytics

### Health Checks
```bash
curl https://your-app-url.com/api/health
```

### Performance Testing
```bash
python performance_test.py
```

### Usage Analytics
- Track API endpoint usage
- Monitor response times
- Log user interactions
- Analyze popular products

## 🔄 Updates and Maintenance

### Updating the Application
1. **Backup current version**
2. **Update code files**
3. **Install new dependencies**: `pip install -r requirements.txt`
4. **Restart the application**
5. **Test functionality**

### Database Maintenance
- Regular backups (if using database features)
- Clean up old logs and temporary files
- Monitor disk space usage

### API Maintenance
- Monitor external API changes
- Update API endpoints if needed
- Handle API rate limits gracefully

---

**Your Whatnot Price Checker is now ready for deployment! 🚀**

