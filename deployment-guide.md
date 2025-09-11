# 🚀 LiveRoom AI Deployment Guide

## 📋 Pre-Deployment Checklist

### 1. Environment Variables Setup

**Backend (.env.production):**
```
DATABASE_URL=postgresql://username:password@host:port/database
OPENAI_API_KEY=sk-proj-your-openai-key
CORS_ORIGINS=https://your-frontend-domain.vercel.app
SECRET_KEY=your-secret-key-here
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=https://your-backend-domain.railway.app
```

### 2. Update CORS Settings

In `LiveRoomBot-Backend/app/main.py`, update CORS origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Database Migration Script

Create `LiveRoomBot-Backend/migrate.py`:
```python
from app.database import engine
from app.models import Base

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    create_tables()
```

## 🚀 Deployment Steps

### Option 1: Vercel + Railway (Recommended)

#### Frontend Deployment (Vercel):
1. Push code to GitHub
2. Go to vercel.com → Import Project
3. Select your repository
4. Configure:
   - Framework: Next.js
   - Root Directory: `LiveRoomBot-Frontend`
   - Build Command: `npm run build`
5. Add environment variables
6. Deploy!

#### Backend Deployment (Railway):
1. Go to railway.app → New Project
2. Deploy from GitHub repo
3. Select `LiveRoomBot-Backend` folder
4. Add PostgreSQL service
5. Configure environment variables
6. Deploy!

### Option 2: Netlify + Render (Free Alternative)

#### Frontend (Netlify):
1. Go to netlify.com → New site from Git
2. Select repository and `LiveRoomBot-Frontend` folder
3. Build command: `npm run build`
4. Publish directory: `.next`
5. Deploy!

#### Backend (Render):
1. Go to render.com → New Web Service
2. Connect GitHub repository
3. Select `LiveRoomBot-Backend` folder
4. Runtime: Python 3
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add PostgreSQL database
8. Deploy!

## 🔧 Post-Deployment Setup

### 1. Initialize Database
Run the database creation script on your deployed backend:
```bash
python create_subcategories_database.py
```

### 2. Test API Endpoints
- Test: `https://your-backend-url/api/v1/characters/`
- Test: `https://your-backend-url/api/v1/subcategories/`

### 3. Update Frontend API URL
Make sure your frontend is pointing to the correct backend URL.

### 4. Test Complete Flow
1. Visit your deployed frontend
2. Navigate through categories
3. Test character selection
4. Test chat functionality

## 💡 Tips for Success

1. **Use Environment Variables** for all sensitive data
2. **Test Locally First** before deploying
3. **Monitor Logs** during deployment
4. **Use HTTPS** for all connections
5. **Set up Custom Domain** for professional look

## 🆘 Troubleshooting

### Common Issues:
- **CORS Errors**: Update CORS origins in backend
- **Database Connection**: Check DATABASE_URL format
- **API Not Found**: Verify backend URL in frontend
- **Build Failures**: Check dependencies and build commands

### Debug Commands:
```bash
# Check backend logs
railway logs

# Test API locally
curl https://your-backend-url/api/v1/health

# Check frontend build
npm run build
```

## 🎉 Success!

Once deployed, your LiveRoom AI platform will be live at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-api.railway.app`

Share your adult AI companion platform with the world! 🔥💋
