# 🚀 Railway Deployment Guide

## ✅ Aplikasi Sudah Siap untuk Railway!

Aplikasi Anda sudah dimodifikasi untuk deployment ke Railway. Berikut adalah file-file yang sudah dibuat:

### 📁 File yang Sudah Dimodifikasi:

- ✅ `app.py` - Updated untuk production
- ✅ `requirements.txt` - Added gunicorn
- ✅ `Procfile` - Untuk Railway deployment
- ✅ `runtime.txt` - Python version
- ✅ `railway.json` - Railway configuration

## 🚀 Step-by-Step Deployment ke Railway

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Login ke Railway

```bash
railway login
```

### Step 3: Deploy dari Folder Anda

```bash
# Dari folder D:\replicate-app
railway up
```

### Step 4: Set Environment Variables

```bash
# Set API Token
railway variables set REPLICATE_API_TOKEN=your_token_here

# Set Secret Key
railway variables set SECRET_KEY=your_secret_key_here

# Set Environment
railway variables set FLASK_ENV=production
```

## 🔧 Environment Variables yang Diperlukan

| Variable              | Description                 | Example                                    |
| --------------------- | --------------------------- | ------------------------------------------ |
| `REPLICATE_API_TOKEN` | Token API Replicate         | `r8_MKvmf9XcInzr6jf4bYz7qdFnJLt9axO05A0yl` |
| `SECRET_KEY`          | Flask secret key            | `your-secret-key-here`                     |
| `FLASK_ENV`           | Environment mode            | `production`                               |
| `PORT`                | Port (Railway set otomatis) | `5000`                                     |

## 🌐 Alternative: Deploy via GitHub

### Step 1: Push ke GitHub

```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### Step 2: Connect ke Railway

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway akan auto-detect Python dan deploy

### Step 3: Set Environment Variables

Di Railway dashboard:

1. Go to your project
2. Click "Variables" tab
3. Add variables:
   ```
   REPLICATE_API_TOKEN=your_token_here
   SECRET_KEY=your_secret_key_here
   FLASK_ENV=production
   ```

## 🔍 Troubleshooting

### Error: "Module not found"

```bash
# Pastikan requirements.txt sudah benar
pip install -r requirements.txt
```

### Error: "Port already in use"

```bash
# Railway akan set PORT otomatis
# Pastikan app.py menggunakan os.environ.get('PORT', 5000)
```

### Error: "Secret key not set"

```bash
# Set SECRET_KEY di Railway dashboard
railway variables set SECRET_KEY=your_secret_key_here
```

## 📊 Monitoring

### View Logs

```bash
railway logs
```

### Check Status

```bash
railway status
```

### Open App

```bash
railway open
```

## 🎯 Expected Result

Setelah deployment sukses, Anda akan mendapat URL seperti:

```
https://your-app-name.railway.app
```

Aplikasi akan berjalan dengan:

- ✅ AI recommendations working
- ✅ Catalog analysis working
- ✅ All features functional
- ✅ Production-ready

## 🆘 Support

Jika ada masalah:

1. Check logs: `railway logs`
2. Check variables: `railway variables`
3. Check status: `railway status`

---

**Selamat! Aplikasi Anda siap untuk production! 🎉**
