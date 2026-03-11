# 🏗️ Summify Architecture & Development Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (HTML/CSS/JS)                  │
│  - Landing Page                                             │
│  - File Upload Interface                                    │
│  - Results Display                                          │
│  - Share & Navigation                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/JSON
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│  ├── /analyze (POST)        - Upload & Process PDF         │
│  ├── /pack/{id} (GET)       - Retrieve Summary             │
│  ├── /pack/{id}/html (GET)  - View as HTML Page            │
│  └── /health (GET)          - Health Check                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
    ┌────────┐   ┌──────────┐   ┌──────────────┐
    │SQLite  │   │OpenAI    │   │pdfplumber    │
    │DB      │   │API       │   │PDF Parsing   │
    └────────┘   └──────────┘   └──────────────┘
```

## 📁 Component Details

### Backend Components

#### `main.py` - FastAPI Application
- **Purpose**: Core web server and API endpoints
- **Key Functions**:
  - `root()` - Serves landing page
  - `analyze()` - Processes PDF uploads
  - `get_pack()` - Returns JSON summary
  - `get_pack_html()` - Returns formatted HTML page
  - `health()` - Health check endpoint
- **Dependencies**: FastAPI, pdfplumber, ai_tools, database
- **Port**: 8000 (default)

#### `ai_tools.py` - AI Integration
- **Purpose**: OpenAI API integration for content generation
- **Key Functions**:
  - `generate_study_material()` - Main orchestrator
  - `_generate_summary()` - Create summary
  - `_generate_insights()` - Extract key points
  - `_generate_flashcards()` - Create study cards
  - `_generate_questions()` - Generate discussion questions
  - `_generate_action_points()` - Extract action items
- **Model**: gpt-3.5-turbo
- **API Calls**: 5 per document (1 for each content type)

#### `database.py` - Data Persistence
- **Purpose**: SQLite database management
- **Key Functions**:
  - `init_db()` - Create tables on startup
  - `save_summary_pack()` - Store generated content
  - `get_summary_pack()` - Retrieve by ID
- **Schema**:
  - `summary_packs` table with 9 columns
  - Auto-increment views tracking
  - Timestamps for created_at metadata

### Frontend Components

#### `index.html` - Landing Page
- **Sections**:
  1. Navigation bar with branding
  2. Hero section with CTA
  3. Features grid (6 features)
  4. Upload/demo section
  5. Footer with links
- **Interactive Elements**:
  - Upload zone (drag & drop)
  - File input (click to browse)
  - Loading states
  - Error messages
  - Result display

#### `app.js` - Client Logic
- **Key Functions**:
  - `handleFileSelect()` - Process file selection
  - `handleDrop()` - Handle drag & drop
  - `showLoading()` - Display loading UI
  - `showResult()` - Render results
  - `copyShareLink()` - Copy to clipboard
  - `resetUpload()` - Reset form
- **API Calls**: POST /analyze, Display results
- **UX Features**: Loading states, error handling, animations

#### `style.css` - Styling & Animations
- **Utilities**: Tailwind-compatible classes
- **Animations**:
  - Slide-in effects
  - Fade transitions
  - Flip animation for flashcards
  - Hover effects
- **Responsive**: Mobile-first design
- **Theme**: Dark mode with purple/pink accents

## 🔄 Data Flow

### Upload and Analysis Flow
```
1. User selects PDF
   ↓
2. JavaScript validates file
   ↓
3. FormData sent to /analyze endpoint
   ↓
4. Backend extracts text with pdfplumber
   ↓
5. AI tools called 5 times (parallel-optimized)
   - Summary generation
   - Insights extraction
   - Flashcard creation
   - Questions generation
   - Action points extraction
   ↓
6. Results saved to SQLite with unique ID
   ↓
7. JSON response sent to frontend
   ↓
8. Results rendered in HTML/CSS
   ↓
9. User sees summary pack with shareable link
```

### Share/View Flow
```
1. User copies /pack/{id}/html link
   ↓
2. Recipient opens in browser
   ↓
3. Backend retrieves from database
   ↓
4. Renders as standalone HTML page
   ↓
5. Recipient sees results (no file needed)
```

## 🧪 Testing & Development

### Manual Testing Checklist
- [ ] Upload small PDF (< 5MB)
- [ ] Test drag & drop interface
- [ ] Verify loading spinner appears
- [ ] Check results render correctly
- [ ] Test share link functionality
- [ ] Verify flashcard flip animation
- [ ] Test on mobile browser
- [ ] Test with corrupted PDF (error handling)

### Load Testing
```bash
# Using Apache Bench (AB)
ab -n 100 -c 10 http://localhost:8000/

# Using hey
hey -n 1000 -c 50 -T "multipart/form-data" \
  -F "file=@test.pdf" http://localhost:8000/analyze
```

### Debug Mode
```python
# In main.py
app = FastAPI(debug=True)  # Enable debug mode
```

## 📦 Dependencies Explained

### Backend Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.104.1 | Web framework |
| uvicorn | 0.24.0 | ASGI server |
| pdfplumber | 0.10.3 | PDF extraction |
| openai | 1.3.5 | GPT API client |
| python-multipart | 0.0.6 | File upload support |
| pydantic | 2.5.0 | Data validation |
| sqlalchemy | 2.0.23 | ORM (optional) |

### No Frontend Build Required!
- Uses Tailwind CSS via CDN (no npm needed)
- Vanilla JavaScript (no framework)
- Direct HTML serving

## 🚀 Performance Optimization

### Current Optimizations
1. **Text Truncation**: Limits PDF to first 50 pages
2. **Token Management**: Truncates text to 3000 chars per API call
3. **Async Processing**: FastAPI handles concurrent requests
4. **Efficient Parsing**: pdfplumber is optimized for speed

### Future Optimization Ideas
1. **Caching**: Redis for frequently accessed packs
2. **Batch Processing**: Queue long documents
3. **Response Compression**: gzip for API responses
4. **Database Indexing**: Index on pack ID and creation date
5. **CDN**: Serve static files from CDN
6. **Worker Pool**: Use Celery for background tasks

## 🔐 Security Features

### Implemented
- File type validation (PDF only)
- File size limits (50MB max)
- Temporary file cleanup
- Input sanitization with Pydantic
- CORS headers configured
- Environment variable for API keys

### Recommended for Production
- Add authentication (JWT/OAuth)
- Rate limiting per IP
- SQL injection prevention (already using parameterized queries)
- HTTPS enforcement
- API key rotation
- Input content scanning
- Data encryption at rest
- Audit logging

## 📊 Database Schema

```sql
CREATE TABLE summary_packs (
    id TEXT PRIMARY KEY,                    -- UUID, short version
    filename TEXT NOT NULL,                 -- Original PDF name
    summary TEXT NOT NULL,                  -- AI summary
    key_insights TEXT NOT NULL,             -- JSON array of strings
    flashcards TEXT NOT NULL,               -- JSON array of objects
    questions TEXT NOT NULL,                -- JSON array of strings
    action_points TEXT NOT NULL,            -- JSON array of objects
    created_at TIMESTAMP DEFAULT NOW(),     -- Creation time
    views INTEGER DEFAULT 0                 -- View counter
);
```

## 🔧 Configuration Options

### Environment Variables
```bash
OPENAI_API_KEY          # Required - OpenAI API key
BASE_URL               # Optional - For share links
DEBUG                  # Optional - Debug mode
```

### Tunable Parameters (in code)
```python
# ai_tools.py
model="gpt-3.5-turbo"          # Change model
max_tokens=400                  # Control response length
temperature=0.7                 # Adjust creativity

# main.py  
max_pdf_pages = 50              # Limit pages processed
temp_path = "/tmp/temp_upload.pdf"  # Temp storage location
```

## 🌍 Internationalization (i18n) Ready

Current: English only
Future: Add i18n by:
1. Extract strings to JSON files
2. Create language-specific files
3. Use JavaScript i18n library
4. Support multiple OpenAI languages

## 📚 Code Conventions

### Python
- PEP 8 compliant
- Type hints encouraged
- Docstrings for functions
- Error handling with try/except

### JavaScript
- Vanilla JS (ES6+)
- const/let preferred over var
- Arrow functions for callbacks
- Error handling in async/await

### HTML/CSS
- Semantic HTML5
- Tailwind CSS classes
- Mobile-first responsive design
- WCAG accessibility ready

## 🐛 Known Limitations

1. **PDF Parsing**: Text-based PDFs only (scanned PDFs need OCR)
2. **Text Extraction**: 50-page limit to manage costs
3. **Concurrent Users**: Depends on OpenAI API rate limits
4. **Storage**: SQLite for small-scale (use PostgreSQL at scale)
5. **Analytics**: No built-in usage tracking

## 🚀 Scaling Strategies

### Phase 1 (0-1000 users)
- Current setup fine
- Monitor API costs

### Phase 2 (1000-10k users)
- Migrate to PostgreSQL
- Add Redis caching
- Implement rate limiting
- Set up CDN

### Phase 3 (10k+ users)
- Kubernetes deployment
- Distributed API handling
- Database replication
- Advanced monitoring

## 📖 Useful Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [OpenAI API Guide](https://platform.openai.com/docs)
- [pdfplumber Docs](https://github.com/jsvine/pdfplumber)
- [Tailwind CSS](https://tailwindcss.com/)
- [SQLite Guide](https://www.sqlite.org/docs.html)

---

**Last Updated**: March 2024  
**Status**: Production Ready  
**Version**: 1.0.0
