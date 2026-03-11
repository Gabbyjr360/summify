# 🌐 Deployment Guide

Deploy Summify to production in minutes. Choose your platform below.

## Quick Deployment (Recommended for beginners)

### Option 1: Render.com (Easiest)

**Step 1: Connect GitHub**
1. Push your code to GitHub
2. Go to render.com
3. Click "New +" → "Web Service"
4. Connect your GitHub repo

**Step 2: Configure**
- Build Command: `pip install -r requirements.txt`
- Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

**Step 3: Environment Variables**
Add in Settings:
```
OPENAI_API_KEY=sk-your-key-here
BASE_URL=https://your-app.onrender.com
```

**Step 4: Deploy**
- Click "Deploy"
- Wait 2-3 minutes
- Your app is live at `https://your-app.onrender.com`

---

### Option 2: Railway.app

**Step 1: Initialize**
```bash
cd /path/to/summify
railway init
railway link  # Link to your project
```

**Step 2: Create files**

Create `Procfile`:
```
web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Step 3: Set Environment**
```bash
railway variables set OPENAI_API_KEY=sk-your-key
```

**Step 4: Deploy**
```bash
railway up
```

---

### Option 3: Heroku (Classic)

**Step 1: Install Heroku CLI**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

**Step 2: Create files**

`Procfile`:
```
web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

`runtime.txt`:
```
python-3.11.0
```

**Step 3: Deploy**
```bash
heroku login
heroku create summify-yourname
git push heroku main
heroku config:set OPENAI_API_KEY=sk-your-key
```

---

## Advanced Deployment (Production)

### Docker Deployment

**Step 1: Create Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV OPENAI_API_KEY=""
ENV PORT=8000

EXPOSE $PORT

CMD ["sh", "-c", "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT"]
```

**Step 2: Build & Run**

```bash
# Build
docker build -t summify .

# Run locally
docker run -e OPENAI_API_KEY=sk-your-key -p 8000:8000 summify

# Push to Docker Hub
docker tag summify yourusername/summify
docker push yourusername/summify
```

**Step 3: Deploy to Container Services**
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

---

### Kubernetes Deployment

**Step 1: Create `k8s/deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: summify
spec:
  replicas: 3
  selector:
    matchLabels:
      app: summify
  template:
    metadata:
      labels:
        app: summify
    spec:
      containers:
      - name: summify
        image: yourusername/summify:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: summify-secrets
              key: api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: summify-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: summify
```

**Step 2: Deploy**

```bash
# Create secret
kubectl create secret generic summify-secrets \
  --from-literal=api-key=sk-your-key

# Deploy
kubectl apply -f k8s/deployment.yaml

# Check status
kubectl get pods
kubectl logs [pod-name]
```

---

### AWS Elastic Beanstalk

**Step 1: Create `.ebextensions/python.config`**

```yaml
option_settings:
  aws:autoscaling:asg:
    MinSize: 2
    MaxSize: 6
  aws:elasticbeanstalk:container:python:
    WSGIPath: backend/main:app
```

**Step 2: Deploy**

```bash
pip install awsebcli-ce
eb init -p python-3.11 summify
eb create summify-prod
eb setenv OPENAI_API_KEY=sk-your-key
eb deploy
```

---

### Google Cloud Run

**Step 1: Create `cloudrun.yaml`**

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: summify
spec:
  template:
    spec:
      containers:
      - image: gcr.io/[PROJECT_ID]/summify
        env:
        - name: OPENAI_API_KEY
          value: sk-your-key
        resources:
          limits:
            memory: 512Mi
            cpu: 1
```

**Step 2: Deploy**

```bash
gcloud run deploy summify \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=sk-your-key
```

---

## Database Migration (SQLite → PostgreSQL)

### Step 1: Install PostgreSQL adapter

```bash
pip install psycopg2-binary
```

### Step 2: Update database.py connection

```python
import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/summify")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)
```

### Step 3: Set database URL

```bash
# On deployment platform
DATABASE_URL=postgresql://user:pass@host:5432/summify
```

---

## Custom Domain Setup

### Option 1: Render.com
1. Go to Settings → Custom Domains
2. Add your domain (e.g., summify.com)
3. Update DNS records
4. Enable auto-redirect to HTTPS

### Option 2: Cloudflare
1. Add site to Cloudflare
2. Point to your deployment
3. Enable SSL/TLS
4. Set up email routing if needed

### Option 3: AWS Route53
1. Create hosted zone
2. Point DNS to your app
3. Create SSL certificate with ACM
4. Map in API Gateway

---

## Monitoring & Logging

### Sentry Error Tracking

**Setup:**
```bash
pip install sentry-sdk
```

**In main.py:**
```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://your-dsn@sentry.io/project-id",
    traces_sample_rate=1.0
)
```

### LogRocket Frontend Monitoring

Add to index.html:
```html
<script src="https://cdn.lr-ingest.com/LogRocket.min.js"></script>
<script>
  window.LogRocket && window.LogRocket.getSessionURL(sessionURL => {
    console.log(`LogRocket Session URL: ${sessionURL}`);
  });
</script>
```

### Google Analytics

Add to index.html:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_ID');
</script>
```

---

## Performance Optimization

### Enable Gzip Compression

```python
from fastapi.middleware.gzip import GZIPMiddleware

app.add_middleware(GZIPMiddleware, minimum_size=1000)
```

### Add Caching Headers

```python
from fastapi.responses import FileResponse

@app.get("/static/{file_path:path}")
async def serve_static(file_path: str):
    return FileResponse(
        file_path,
        headers={
            "Cache-Control": "public, max-age=31536000"
        }
    )
```

### Enable CORS with specific origins

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://summify.com",
        "https://www.summify.com"
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## Backup & Disaster Recovery

### Option 1: Automated Backups

```bash
# SQLite backup script
cp backend/summify.db backend/summify.db.backup.$(date +%s)

# Upload to S3
aws s3 cp backend/summify.db.backup.* s3://summify-backups/
```

### Option 2: Cloud Database Backups

**AWS RDS:**
- Automated backups: 7 days (configurable)
- Manual snapshots anytime
- Point-in-time recovery available

**Google Cloud SQL:**
- Automated backups: configurable retention
- On-demand backups
- Backup location options

---

## SSL/TLS Certificate

### Let's Encrypt (Free)

```bash
pip install certbot certbot-nginx

certbot certonly --standalone -d summify.com -d www.summify.com
```

### AWS Certificate Manager (Free for AWS)

1. Go to ACM
2. Request certificate
3. Validate domain
4. Attach to distribution

---

## Scaling Strategies

### Horizontal Scaling
- Add more server instances
- Use load balancer (ALB/NLB)
- Distribute traffic evenly

### Vertical Scaling  
- Increase CPU/RAM per instance
- Upgrade to premium tier
- Optimize slow queries

### Database Scaling
- Read replicas for queries
- Connection pooling (PgBouncer)
- Sharding for large datasets

---

## Cost Optimization

### Reduce API Costs
- Cache common documents
- Batch process documents
- Use gpt-3.5-turbo (cheaper than gpt-4)

### Reduce Hosting Costs
- Use free tier while under limits
- Reserved instances for consistent load
- Spot instances for development

### Reduce Bandwidth Costs
- Enable compression
- Minify assets
- Use CDN for static files

---

## Troubleshooting Deployment

### Deploy fails with "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### App crashes on startup
```bash
# Check logs
git log --oneline -n 20
eb logs
# Or
docker logs [container-id]
```

### Database connection error
```bash
# Verify DATABASE_URL is set
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"
```

### API not responding  
- Check if server is running
- Verify port is exposed (8000)
- Check firewall rules

---

## Next Steps

1. Choose your deployment platform
2. Follow the setup instructions
3. Test in production
4. Set up monitoring
5. Configure backups
6. Celebrate! 🎉

For more help, see:
- Platform documentation
- DEVELOPMENT.md
- GitHub Issues

Happy deploying!
