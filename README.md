# Summify - AI Document Intelligence Platform

A modern, production-ready AI SaaS application that analyzes PDFs and generates intelligent summaries, insights, flashcards, and questions using OpenAI's API.

![Summify Demo](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Features

### Core Capabilities
- **AI-Powered Summaries** - Get clear, concise overviews of any document
- **Key Insights** - Automatically extract important bullet points
- **Smart Flashcards** - Create learning cards for memorization  
- **Discussion Questions** - Generate thoughtful questions about documents
- **Action Points** - Get practical takeaways and next steps

### Technical Features
- **Modern SaaS UI** - Beautiful, responsive design with Tailwind CSS
- **Drag & Drop Upload** - Simple file upload with visual feedback
- **Shareable Links** - Generate public URLs for each summary pack
- **SQLite Database** - Persistent storage of all generated summaries
- **Real-time Processing** - Fast AI analysis with loading states
- **Mobile Responsive** - Works perfectly on desktop, tablet, and mobile

## 📋 Project Structure

```
summify/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── ai_tools.py          # OpenAI integration
│   ├── database.py          # SQLite management
│   └── __pycache__/
├── frontend/
│   ├── index.html           # Landing page & upload UI
│   ├── app.js              # Client-side logic
│   └── style.css           # Custom styling
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **pdfplumber** - PDF text extraction
- **OpenAI API** - GPT-3.5-Turbo for AI analysis
- **SQLite** - Lightweight database
- **Uvicorn** - ASGI server

### Frontend
- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first CSS framework
- **Vanilla JavaScript** - No framework dependencies
- **CSS3** - Modern animations and effects

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- OpenAI API key

### Step 1: Get an OpenAI API Key
1. Go to https://platform.openai.com/api_keys
2. Create a new API key
3. Copy your API key

### Step 2: Clone/Setup Project
```bash
cd /home/gabriel/Desktop/summify
```

### Step 3: Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt
```

### Step 4: Set Environment Variables
```bash
# On Linux/Mac
export OPENAI_API_KEY="your-api-key-here"

# On Windows (CMD)
set OPENAI_API_KEY=your-api-key-here

# On Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"
```

### Step 5: Run the Application
```bash
# Navigate to backend directory
cd backend

# Start the server
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at: **http://localhost:8000**

## 🎯 Usage

1. **Open the Application**
   - Navigate to `http://localhost:8000` in your browser

2. **Upload a Document**
   - Click "Upload PDF Now" or drag a PDF into the upload zone
   - Wait for AI processing (usually 10-30 seconds)

3. **Review Results**
   - View Summary, Key Insights, Flashcards, Questions, and Action Points
   - Click flashcards to flip and see answers

4. **Share Your Summary**
   - Click the "Copy" button to get your shareable link
   - Share with anyone using the public URL
   - Recipients can view your summary without uploading

## 🔌 API Endpoints

### POST /analyze
Upload a PDF and generate a Smart Summary Pack.

**Request:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "success": true,
  "pack_id": "abc123def456",
  "message": "Smart Summary Pack generated successfully!",
  "result": {
    "summary": "...",
    "key_insights": [...],
    "flashcards": [...],
    "questions": [...],
    "action_points": [...]
  }
}
```

### GET /pack/{pack_id}
Retrieve a generated summary pack as JSON.

**Request:**
```bash
curl "http://localhost:8000/pack/abc123def456"
```

**Response:**
```json
{
  "id": "abc123def456",
  "filename": "document.pdf",
  "summary": "...",
  "key_insights": [...],
  "flashcards": [...],
  "questions": [...],
  "action_points": [...],
  "created_at": "2024-03-11 12:34:56",
  "views": 5
}
```

### GET /pack/{pack_id}/html
View a summary pack as an HTML page (for sharing).

## 🎨 UI Components

### Landing Page
- **Hero Section** - Eye-catching headline and CTA
- **Features Grid** - 6 key features displayed visually
- **Upload Section** - Drag-and-drop interface
- **Footer** - Company info and links

### Result Page
- **Summary Section** - Clear overview of document
- **Key Insights** - Bullet-point highlights
- **Flashcards** - Clickable learning cards (flip animation)
- **Discussion Questions** - Engaging questions for study
- **Action Points** - Practical takeaways
- **Share Section** - Copy and share your summary

### Pack View Page
- Clean presentation of generated content
- Shareable URL with metadata
- All features accessible without creating account

## 🔒 Security Considerations

1. **API Key Management**
   - Never commit API keys to version control
   - Use environment variables or `.env` files
   - Rotate keys periodically

2. **File Handling**
   - PDFs are processed in memory and not stored
   - Temporary files are cleaned up automatically
   - File size limit: 50MB

3. **Database**
   - SQLite backs up automatically
   - Consider migrating to PostgreSQL for production
   - Implement user authentication for private summaries

## 🚀 Deployment

### Simple Deployment (Render, Heroku, Railway)

1. **Create `.env` file:**
```env
OPENAI_API_KEY=your-api-key
BASE_URL=https://your-domain.com
```

2. **Create `Procfile`:**
```
web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

3. **Create `runtime.txt`:**
```
python-3.11.0
```

4. **Deploy to your platform:**
   - Connect your GitHub repository
   - Set environment variables
   - Deploy!

### Production Recommendations

1. **Database**
   - Migrate from SQLite to PostgreSQL
   - Implement connection pooling
   - Set up automated backups

2. **Caching**
   - Add Redis for frequently accessed packs
   - Cache OpenAI responses temporarily

3. **Monitoring**
   - Set up error tracking (Sentry)
   - Monitor API usage
   - Track performance metrics

4. **Scaling**
   - Use async task queue (Celery)
   - Process large PDFs in background
   - Implement rate limiting

## 🐛 Troubleshooting

### "OpenAI API Key Not Found"
```bash
# Verify key is set
echo $OPENAI_API_KEY

# If not set, run:
export OPENAI_API_KEY="sk-..."
```

### "PDF Processing Failed"
- Ensure PDF is not corrupted
- Try with a smaller PDF first
- Check that pdfplumber is installed: `pip install pdfplumber`

### "Connection Refused"
- Verify server is running on port 8000
- Check firewall settings
- Try different port: `uvicorn main:app --port 8001`

### "ModuleNotFoundError"
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

## 📈 Performance Tips

1. **Faster Processing**
   - Smaller PDFs process faster (keep under 50MB)
   - First request may take longer while model loads
   - Subsequent requests cache results

2. **Optimal AI Settings**
   - Using gpt-3.5-turbo for speed and cost
   - Adjust temperature (0.7) for different outputs
   - Limit tokens for faster responses

## 🔄 Roadmap

### v2.0 (Planned)
- [ ] User authentication and accounts
- [ ] Multiple language support
- [ ] Custom AI model selection
- [ ] Advanced document formatting
- [ ] Real-time collaboration
- [ ] Export to PDF/Word
- [ ] Browser extension
- [ ] Mobile apps

### v3.0 (Future)
- [ ] Multi-document analysis
- [ ] Team workspaces
- [ ] Advanced analytics
- [ ] Custom LLM integration
- [ ] Offline support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 💬 Support

For issues and questions:
- Create an Issue on GitHub
- Email: support@summify.ai
- Documentation: https://summify.ai/docs

## 🎓 Use Cases

### Students
- Summarize lecture notes
- Generate study flashcards
- Create exam prep questions

### Professionals
- Extract key insights from reports
- Identify action items
- Prepare meeting notes

### Researchers
- Summarize papers quickly
- Extract key findings
- Compare document insights

### Creators
- Analyze competitor content
- Extract writing inspiration
- Find discussion topics

### Business Users
- Summarize incoming documents
- Extract executive summaries
- Track important information

## 💡 Pro Tips

1. **Flashcard Length** - Create consistent question lengths for better learning
2. **Sharing** - Share summaries with colleagues for collaborative learning
3. **Formats** - Works with PDFs from any source (scanned, digital, web)
4. **Batch Processing** - Upload multiple documents for comprehensive analysis

## 🌟 Star History

Give this project a star if you find it useful!

---

**Made with ❤️ for learners, professionals, and creators everywhere.**

**Ready to transform the way you work with documents? Start using Summify today!**
