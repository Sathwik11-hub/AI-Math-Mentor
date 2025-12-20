# Deployment Guide for AI Math Mentor

## Streamlit Cloud Deployment

### Prerequisites
- GitHub account with the repository
- Streamlit Cloud account (free at share.streamlit.io)

### Steps

1. **Push code to GitHub** (already done)

2. **Go to Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"

3. **Configure the app**
   - Repository: `Sathwik11-hub/AI-Math-Mentor`
   - Branch: `main` (or your deployment branch)
   - Main file path: `app.py`
   - App URL: Choose your custom URL

4. **Add Secrets**
   - Click "Advanced settings" → "Secrets"
   - Add your OpenAI API key:
   ```toml
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (first build takes ~5-10 minutes)

### Configuration
The app will automatically use `.streamlit/config.toml` for theme settings.

---

## HuggingFace Spaces Deployment

### Prerequisites
- HuggingFace account
- Git installed locally

### Steps

1. **Create a new Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Name: `ai-math-mentor`
   - License: MIT
   - SDK: Streamlit
   - Hardware: CPU (free tier)

2. **Clone the Space repository**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/ai-math-mentor
   cd ai-math-mentor
   ```

3. **Copy files from this repository**
   ```bash
   cp -r /path/to/AI-Math-Mentor/* .
   ```

4. **Add secrets**
   - Go to Space Settings → Repository secrets
   - Add: `OPENAI_API_KEY` with your key

5. **Push to HuggingFace**
   ```bash
   git add .
   git commit -m "Deploy AI Math Mentor"
   git push
   ```

---

## Local Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Set environment variables
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run the application
CMD ["streamlit", "run", "app.py"]
```

### Build and Run

```bash
# Build the Docker image
docker build -t ai-math-mentor .

# Run the container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_key_here \
  ai-math-mentor
```

Access at: http://localhost:8501

---

## Render Deployment

### Prerequisites
- Render account (free at render.com)
- GitHub repository connected

### Steps

1. **Create New Web Service**
   - Go to Render Dashboard
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - Name: `ai-math-mentor`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

3. **Add Environment Variables**
   - Add `OPENAI_API_KEY` in Environment section

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

---

## Railway Deployment

### Steps

1. **Install Railway CLI** (optional)
   ```bash
   npm install -g railway
   ```

2. **Deploy via GitHub**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository
   - Railway auto-detects Python and builds

3. **Add Environment Variables**
   - Go to project settings
   - Add `OPENAI_API_KEY`

4. **Configure Port**
   Railway automatically assigns a port. The app will be accessible at the generated URL.

---

## Environment Variables Required

All deployment platforms need these environment variables:

**Required:**
- `OPENAI_API_KEY` - Your OpenAI API key

**Optional (with defaults):**
- `OPENAI_MODEL` - Default: `gpt-4`
- `EMBEDDING_MODEL` - Default: `text-embedding-ada-002`
- `OCR_CONFIDENCE_THRESHOLD` - Default: `0.7`
- `ASR_CONFIDENCE_THRESHOLD` - Default: `0.7`
- `VERIFIER_CONFIDENCE_THRESHOLD` - Default: `0.8`
- `WHISPER_MODEL` - Default: `base` (options: tiny, base, small, medium, large)

---

## Performance Optimization for Deployment

### For Free Tiers
1. Use smaller Whisper model: `WHISPER_MODEL=tiny` or `base`
2. Reduce RAG chunks: `RAG_TOP_K=2`
3. Use lighter embedding model (already using MiniLM)

### For Production
1. Use GPU instances for faster Whisper transcription
2. Cache embeddings and models
3. Consider using paid OpenAI tier for higher rate limits
4. Monitor API costs with OpenAI dashboard

---

## Monitoring & Logs

### Streamlit Cloud
- View logs in app dashboard
- Monitor resource usage in settings

### HuggingFace
- Logs available in Space settings
- Built-in resource monitoring

### Docker
```bash
# View logs
docker logs <container-id>

# Monitor resources
docker stats <container-id>
```

---

## Cost Estimates

### Free Tier (Streamlit Cloud / HF Spaces)
- Hosting: $0
- OpenAI API: ~$0.01-0.05 per problem solved
- Monthly estimate: $5-20 for moderate usage

### Paid Deployment (Production)
- Hosting: $7-25/month (Render/Railway)
- OpenAI API: ~$0.01-0.05 per problem
- Monthly estimate: $30-100 for production usage

---

## Troubleshooting Deployment

### Issue: Out of Memory
**Solution:** 
- Use smaller Whisper model
- Increase deployment RAM (paid tier)
- Disable OCR/ASR if not needed

### Issue: Slow First Load
**Solution:**
- Normal - models download on first run
- Subsequent loads are cached

### Issue: OpenAI API Errors
**Solution:**
- Check API key is correct
- Verify account has credits
- Check rate limits

### Issue: Import Errors
**Solution:**
- Ensure requirements.txt is complete
- Check Python version compatibility (3.8+)

---

## Security Best Practices

1. **Never commit API keys** - Use environment variables
2. **Use secrets management** - Platform-provided secrets
3. **Rate limiting** - Monitor API usage
4. **Input validation** - Already implemented in code
5. **Regular updates** - Keep dependencies updated

---

## Support

For deployment issues:
- Check platform documentation
- Review application logs
- Open GitHub issue with deployment platform tag
