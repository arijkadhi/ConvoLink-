# 💯 100% FREE DEPLOYMENT GUIDE

## ⚠️ IMPORTANT: ALL SERVICES ARE COMPLETELY FREE

This guide focuses **exclusively on FREE options** with no payment required at any stage.

---

## 🎯 Recommended: Render.com (FREE Tier)

**Why Render FREE Tier?**
- ✅ Completely FREE (no credit card required)
- ✅ Automatic HTTPS/SSL
- ✅ Auto-deploy from GitHub
- ✅ FREE PostgreSQL database (optional)
- ✅ 750 hours/month free
- ✅ No time limit on free tier

### Step-by-Step Render Deployment

#### 1. Prepare Your GitHub Repository

```bash
# Make sure your code is pushed to GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/messaging-api.git
git push -u origin main
```

#### 2. Sign Up for Render (FREE)

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (no credit card needed)

#### 3. Create Web Service (FREE)

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select your messaging-api repository
4. Configure:

```yaml
Name: messaging-api
Environment: Python 3
Region: Choose closest to you
Branch: main
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Instance Type: FREE (Select this!)
```

#### 4. Add Environment Variables

Click "Environment" and add:

```env
PYTHON_VERSION=3.11.0
SECRET_KEY=paste-your-generated-secret-key-here
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=sqlite:///./messaging.db
ALLOWED_ORIGINS=https://your-app-name.onrender.com
LOG_LEVEL=INFO
```

**Generate SECRET_KEY** (run locally):
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 5. Deploy (FREE)

1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Your API will be live at: `https://your-app-name.onrender.com`

#### 6. Verify Deployment

Visit these URLs:
- API Root: `https://your-app-name.onrender.com/`
- Health Check: `https://your-app-name.onrender.com/health`
- API Docs: `https://your-app-name.onrender.com/docs`

### Optional: Add FREE PostgreSQL Database

**Note**: SQLite works great for most projects! Only add PostgreSQL if you need it.

1. Click "New +" → "PostgreSQL"
2. Name: messaging-db
3. Database: messaging_api
4. User: messaging_user
5. Region: Same as web service
6. Instance Type: **FREE** (Select this!)
7. Click "Create Database"

8. Copy the "Internal Database URL" 
9. Update your web service environment variable:
   ```env
   DATABASE_URL=<paste-internal-database-url>
   ```

10. Your service will automatically redeploy

---

## 🔄 Auto-Deploy from GitHub (FREE)

Render automatically deploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push origin main

# Render will automatically detect and deploy (2-5 minutes)
```

---

## 📊 GitHub Actions CI/CD (FREE)

Already configured in `.github/workflows/ci-cd.yml`

**What it does (automatically)**:
- ✅ Runs tests on every push
- ✅ Checks code quality
- ✅ Builds Docker image (optional)
- ✅ 100% FREE with GitHub

**No setup needed** - just push to GitHub!

---

## 🗄️ Database Options (Both FREE)

### Option 1: SQLite (Recommended for FREE tier)
- ✅ Already configured by default
- ✅ Zero setup required
- ✅ Perfect for small to medium apps
- ✅ Works great on Render FREE tier
- ⚠️ File-based (stored with application)

**Current configuration** in `.env`:
```env
DATABASE_URL=sqlite:///./messaging.db
```

### Option 2: Render PostgreSQL (FREE tier)
- ✅ FREE tier available (1GB storage)
- ✅ Better for production
- ✅ Automatic backups
- ⚠️ Expires after 90 days of inactivity (just access it to keep alive)

**To use**: Follow "Optional: Add FREE PostgreSQL Database" above

---

## 🧪 Testing Your Deployed API

### Using cURL

```bash
# Replace YOUR_APP_NAME with your Render app name

# 1. Health Check
curl https://YOUR_APP_NAME.onrender.com/health

# 2. Register User
curl -X POST "https://YOUR_APP_NAME.onrender.com/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123"
  }'

# 3. Login
curl -X POST "https://YOUR_APP_NAME.onrender.com/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=TestPass123"

# Copy the access_token from response

# 4. Send Message
curl -X POST "https://YOUR_APP_NAME.onrender.com/api/v1/messages/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_id": 2,
    "content": "Hello from production!"
  }'
```

### Using Insomnia (FREE)

1. Import `insomnia_collection.json`
2. Update environment:
   ```json
   {
     "base_url": "https://YOUR_APP_NAME.onrender.com/api/v1"
   }
   ```
3. Test all endpoints!

---

## 📱 Monitoring (FREE Options)

### 1. UptimeRobot (FREE)
- 50 monitors free
- 5-minute checks
- Email alerts

**Setup**:
1. Go to https://uptimerobot.com
2. Sign up (FREE)
3. Add monitor: `https://your-app-name.onrender.com/health`

### 2. Render Dashboard (FREE)
- Built-in metrics
- View logs in real-time
- No setup needed

**View Logs**:
1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab

---

## 🔧 Troubleshooting FREE Tier

### Issue: "Service spins down after inactivity"
**Solution**: Render FREE tier services sleep after 15 minutes of inactivity
- First request will wake it up (takes 30-60 seconds)
- Use UptimeRobot to ping every 14 minutes (keeps it awake)

### Issue: "Deployment failed"
**Solution**: Check build logs in Render dashboard
- Common issues:
  - Missing dependencies in requirements.txt
  - Wrong Python version
  - Environment variables not set

### Issue: "Database connection error"
**Solution**: 
- Verify DATABASE_URL is correct
- For SQLite: Should be `sqlite:///./messaging.db`
- For PostgreSQL: Use "Internal Database URL" from Render

### Issue: "502 Bad Gateway"
**Solution**:
- Check Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Must use `$PORT` (Render provides this)
- Check logs for Python errors

---

## 💰 Cost Breakdown (ALL FREE!)

| Service | Cost | What You Get |
|---------|------|--------------|
| Render Web Service | **FREE** | 750 hours/month, HTTPS, Auto-deploy |
| Render PostgreSQL | **FREE** | 1GB storage, 90-day inactivity limit |
| SQLite | **FREE** | Unlimited, file-based |
| GitHub Actions | **FREE** | 2,000 minutes/month |
| GitHub Repository | **FREE** | Unlimited public repos |
| Insomnia | **FREE** | Full API testing |
| UptimeRobot | **FREE** | 50 monitors |
| **TOTAL** | **$0.00** | Everything you need! |

---

## ✅ Post-Deployment Checklist

- [ ] API is accessible at Render URL
- [ ] Health endpoint returns 200: `/health`
- [ ] Can register new user
- [ ] Can login and get JWT token
- [ ] Can send messages
- [ ] Can retrieve messages
- [ ] API docs work: `/docs`
- [ ] Set up UptimeRobot monitoring (optional)
- [ ] Add custom domain (optional, FREE with Render)

---

## 🎓 Tips for FREE Tier Success

1. **Keep Service Active**: Use UptimeRobot to ping every 14 minutes
2. **Use SQLite Initially**: Switch to PostgreSQL only if needed
3. **Monitor Usage**: Check Render dashboard for hours used
4. **Optimize Performance**: FREE tier has 512MB RAM (optimize code)
5. **Enable Caching**: Reduce database queries where possible

---

## 🚀 Next Steps

1. **Deploy to Render** (10 minutes)
2. **Test all endpoints** (5 minutes)
3. **Set up monitoring** (5 minutes)
4. **Share your API** with team/professor
5. **Add custom domain** (optional, FREE)

---

## 🆘 Need Help?

- Render Docs: https://render.com/docs
- Check logs in Render dashboard
- Review `tests/` for usage examples
- Open issue on GitHub

**Remember**: Everything is 100% FREE! No credit card, no payment, ever! 🎉
