# Confidra AI - Next.js for Vercel

## Setup

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) with your browser.

## Deploy to Vercel

### Option 1: Vercel CLI (Recommended)

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Follow the prompts to connect your project.

### Option 2: Vercel Dashboard

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your GitHub repository
4. Vercel will automatically detect it's a Next.js project
5. Deploy!

## Environment Variables

Set these in your Vercel project settings:

- `BACKEND_URL`: Your FastAPI backend URL (deployed separately)

## Backend Deployment

You'll also need to deploy your FastAPI backend. Options:

1. **Railway**: Easy Python deployment
2. **Heroku**: Classic platform
3. **DigitalOcean App Platform**: Simple and affordable
4. **AWS Lambda**: Serverless option

## Project Structure

```
confidra-web/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── DocumentUpload.tsx
│   ├── TextInput.tsx
│   └── QuerySection.tsx
├── package.json
├── next.config.js
├── tailwind.config.js
└── vercel.json
```

## Features

- 🌙 Dark theme UI matching your design
- 📁 Document upload (PDF, DOCX, TXT)
- ✏️ Text input for pasting content
- 🔍 NDA risk scanning
- 💬 Interactive Q&A
- 🎨 Modern animations with Framer Motion
- 📱 Responsive design with Tailwind CSS
