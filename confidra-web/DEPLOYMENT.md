# 🚀 Deploy Confidra AI to Vercel

## ✅ What I've Created

I've built a complete **Next.js version** of your Confidra AI dashboard that's ready for Vercel deployment!

### 📁 Project Structure:

```
confidra-web/
├── app/
│   ├── globals.css        # Tailwind CSS styles
│   ├── layout.tsx         # App layout
│   └── page.tsx          # Main page
├── components/
│   ├── DocumentUpload.tsx # File upload component
│   ├── TextInput.tsx     # Text input component
│   └── QuerySection.tsx  # Q&A interface
├── package.json          # Dependencies
├── next.config.js        # Next.js configuration
├── vercel.json          # Vercel deployment config
└── README.md            # Documentation
```

## 🎨 Features Included:

✅ **Exact UI Match**: Dark theme (#1E2A38) with your design  
✅ **Confidra AI Branding**: Logo and styling  
✅ **Document Upload**: PDF, DOCX, TXT support  
✅ **Text Input**: Paste contracts directly  
✅ **Risk Scanning**: Integration with your FastAPI backend  
✅ **Interactive Q&A**: Ask questions about contracts  
✅ **Modern Animations**: Framer Motion effects  
✅ **Responsive Design**: Works on all devices  
✅ **TypeScript**: Type-safe code

## 🚀 Deploy to Vercel (3 Steps):

### Step 1: Deploy Your Backend to Vercel

Your FastAPI backend can now be deployed to Vercel too!

1. **Navigate to backend directory**:

   ```bash
   cd ../backend
   vercel login
   vercel
   ```

2. **Set environment variables**:

   ```bash
   vercel env add OPENAI_API_KEY
   vercel env add FRIENDLI_TOKEN
   ```

3. **Deploy to production**:

   ```bash
   vercel --prod
   ```

4. **Get your backend URL** (e.g., `https://your-backend-abc123.vercel.app`)

### Step 2: Deploy Frontend to Vercel

1. **Push to GitHub**:

   ```bash
   cd confidra-web
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/confidra-ai.git
   git push -u origin main
   ```

2. **Deploy on Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import from GitHub
   - Select your `confidra-ai` repository
   - Vercel auto-detects Next.js settings
   - Click "Deploy"

### Step 3: Configure Environment Variables

In Vercel project settings (Settings → Environment Variables), add:

- `NEXT_PUBLIC_BACKEND_URL`: Your deployed FastAPI backend URL (e.g., `https://your-backend-abc123.vercel.app`)

**Important**: Use the exact backend URL from Step 1 without trailing slash.

## 🔧 Local Development:

```bash
cd confidra-web
npm run dev
```

Visit: `http://localhost:3000`

## 🎯 What Happens After Deployment:

1. **Automatic Builds**: Vercel rebuilds on every GitHub push
2. **Global CDN**: Fast loading worldwide
3. **HTTPS**: Automatic SSL certificates
4. **Custom Domain**: Easy to add your own domain
5. **Analytics**: Built-in performance monitoring

## 🔄 Backend Integration:

The frontend will make API calls to your backend:

- `POST /upload-document` - Process uploaded files
- `POST /ask` - Handle Q&A queries

Make sure your FastAPI backend has CORS enabled for your Vercel domain!

## 📱 Production Ready:

- ✅ Optimized builds
- ✅ Image optimization
- ✅ Code splitting
- ✅ SEO friendly
- ✅ Progressive Web App ready

Your Confidra AI dashboard will be live at:
`https://your-project-name.vercel.app` 🌐
