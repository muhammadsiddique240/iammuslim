# Free Deployment Options for iammuslim Website

## 🚀 **Quick Deployment Guide**

### **Prerequisites Before Deployment:**
1. **Set up your admin user** in Django admin
2. **Configure environment variables** properly
3. **Test locally** with `docker compose up`
4. **Push code to GitHub** repository

---

## 🌐 **1. FREE DEPLOYMENT OPTIONS**

### **Option A: Railway (Recommended - Most Django-Friendly)**

#### **Setup:**
1. **Go to** [Railway.app](https://railway.app) and sign up with GitHub
2. **Connect your GitHub repository**
3. **Railway auto-detects Django** and sets up automatically

#### **Configuration Files Needed:**
```yaml
# railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT"
  }
}
```

```toml
# nixpacks.toml
[phases.setup]
nixPkgs = ["...", "postgresql"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = ["python manage.py collectstatic --noinput"]

[start]
cmd = "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT"
```

#### **Environment Variables:**
```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=0
DATABASE_URL=postgresql://...
DJANGO_ALLOWED_HOSTS=your-app-name.up.railway.app
```

---

### **Option B: Render (Good for Django)**

#### **Setup:**
1. **Go to** [Render.com](https://render.com) and create account
2. **Connect GitHub repository**
3. **Choose "Web Service"**
4. **Select Python environment**

#### **Configuration:**
- **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Start Command:** `gunicorn config.wsgi:application`

#### **Environment Variables:**
```
DJANGO_SECRET_KEY=generate-new-secret
DJANGO_DEBUG=False
DATABASE_URL=postgresql://... (Render provides free PostgreSQL)
DJANGO_ALLOWED_HOSTS=your-app.onrender.com
```

---

### **Option C: Heroku (Classic Choice)**

#### **Setup:**
1. **Install Heroku CLI**
2. **Create Heroku app:** `heroku create your-app-name`
3. **Add PostgreSQL:** `heroku addons:create heroku-postgresql:hobby-dev`

#### **Files Needed:**
```python
# Procfile
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

```python
# runtime.txt
python-3.12.0
```

#### **Deploy:**
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

### **Option D: Vercel (For Static Parts)**

#### **Setup:**
1. **Go to** [Vercel.com](https://vercel.com) and connect GitHub
2. **Vercel auto-detects Django** and handles deployment

#### **Configuration:**
- **Framework:** Python
- **Install Command:** `pip install -r requirements.txt`
- **Build Command:** `python manage.py collectstatic --noinput`
- **Start Command:** `gunicorn config.wsgi:application`

---

## 🗄️ **2. DATABASE OPTIONS**

### **Free Database Options:**
1. **Railway PostgreSQL** - Free tier included
2. **Render PostgreSQL** - Free tier included
3. **Supabase** - Free PostgreSQL database
4. **ElephantSQL** - Free PostgreSQL hosting
5. **Neon.tech** - Free PostgreSQL serverless

---

## 🌍 **3. DOMAIN & SSL**

### **Free Custom Domain Options:**
1. **Railway** - Provides SSL certificate automatically
2. **Render** - Free SSL with custom domains
3. **Vercel** - Free SSL and custom domains
4. **Cloudflare Pages** - Free SSL and custom domain

---

## 📋 **4. DEPLOYMENT CHECKLIST**

### **Before Deployment:**
- [ ] **Create GitHub repository**
- [ ] **Push all code to GitHub**
- [ ] **Set up admin user locally**
- [ ] **Test all features locally**
- [ ] **Configure environment variables**

### **Environment Variables Required:**
```bash
DJANGO_SECRET_KEY=generate-secure-key
DJANGO_DEBUG=False
DATABASE_URL=your-database-url
DJANGO_ALLOWED_HOSTS=your-domain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain.com
```

### **Database Migration:**
```bash
# Run after first deployment
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

## 🚀 **5. RECOMMENDED DEPLOYMENT FLOW**

### **Step 1: Choose Platform**
I recommend **Railway** for easiest Django deployment.

### **Step 2: Prepare Code**
```bash
# Create GitHub repository
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/iammuslim.git
git push -u origin main
```

### **Step 3: Deploy**
1. Sign up at Railway.app
2. Connect GitHub repository
3. Railway auto-deploys
4. Set environment variables
5. Run database migrations

### **Step 4: Configure Domain (Optional)**
- Buy cheap domain (~$10/year)
- Point DNS to Railway/Render
- Enable SSL certificate

---

## ⚠️ **6. IMPORTANT NOTES**

### **Security:**
- **Never commit secrets** to GitHub
- **Use environment variables** for sensitive data
- **Enable HTTPS** for production
- **Keep Django DEBUG=False** in production

### **Performance:**
- **Enable caching** for Quran API endpoints
- **Use CDN** for static files (Cloudflare free)
- **Optimize images** before upload
- **Enable compression** in web server

### **Maintenance:**
- **Regular backups** of database
- **Monitor logs** for errors
- **Update dependencies** regularly
- **Test features** after updates

---

## 🎯 **7. QUICK START COMMANDS**

### **Railway Deployment:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link
railway up

# Set environment variables
railway variables set DJANGO_SECRET_KEY=your-key-here
railway variables set DJANGO_DEBUG=0
```

### **Render Deployment:**
```bash
# Deploy via GitHub integration
# Set environment variables in Render dashboard
# Deploy automatically on git push
```

---

## 📞 **8. SUPPORT**

If you encounter issues:
1. **Check deployment logs**
2. **Verify environment variables**
3. **Test database connection**
4. **Check static files serving**
5. **Verify Quran JSON files are accessible**

**Your website will be live at:** `https://your-app-name.railway.app`
