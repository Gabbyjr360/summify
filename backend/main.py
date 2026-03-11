from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import os
from pathlib import Path
import json

try:
    from .ai_tools import generate_study_material
    from .database import save_summary_pack, get_summary_pack, init_db
except ImportError:
    from ai_tools import generate_study_material
    from database import save_summary_pack, get_summary_pack, init_db

# Initialize FastAPI app
app = FastAPI(title="Summify - AI Document Intelligence")

# Initialize database
init_db()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

@app.get("/")
async def root():
    """Serve the landing page."""
    frontend_path = Path(__file__).parent.parent / "frontend" / "index.html"
    if frontend_path.exists():
        with open(frontend_path, "r") as f:
            return HTMLResponse(content=f.read())
    return {"message": "Summify API is running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """
    Upload a PDF and generate smart summary pack.
    Returns pack ID for sharing.
    """
    try:
        # Validate file type
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Extract text from PDF
        text = ""
        contents = await file.read()
        
        # Save temporarily to read with pdfplumber
        temp_path = "/tmp/temp_upload.pdf"
        with open(temp_path, "wb") as f:
            f.write(contents)
        
        try:
            with pdfplumber.open(temp_path) as pdf:
                # Limit to first 50 pages to avoid token limits
                for i, page in enumerate(pdf.pages):
                    if i >= 50:
                        break
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Generate AI insights
        result = generate_study_material(text)
        
        # Save to database
        pack_id = save_summary_pack(
            filename=file.filename,
            summary=result["summary"],
            key_insights=result["key_insights"],
            flashcards=result["flashcards"],
            questions=result["questions"],
            action_points=result["action_points"]
        )
        
        return {
            "success": True,
            "pack_id": pack_id,
            "message": "Smart Summary Pack generated successfully!",
            "result": result
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.get("/pack/{pack_id}")
async def get_pack(pack_id: str):
    """View a public summary pack."""
    pack = get_summary_pack(pack_id)
    
    if not pack:
        raise HTTPException(status_code=404, detail="Summary pack not found")
    
    return JSONResponse(content=pack)

@app.get("/pack/{pack_id}/html")
async def get_pack_html(pack_id: str):
    """Get a summary pack as HTML page for viewing."""
    pack = get_summary_pack(pack_id)
    
    if not pack:
        raise HTTPException(status_code=404, detail="Summary pack not found")
    
    # Generate HTML
    flashcards_html = ""
    if isinstance(pack["flashcards"], list):
        for i, card in enumerate(pack["flashcards"]):
            if isinstance(card, dict):
                question = card.get("question", "")
                answer = card.get("answer", "")
            else:
                question = str(card)
                answer = ""
            
            flashcards_html += f"""
            <div class="flashcard" onclick="this.classList.toggle('flipped')" data-index="{i}">
                <div class="flashcard-inner">
                    <div class="flashcard-front">
                        <p>{question}</p>
                    </div>
                    <div class="flashcard-back">
                        <p>{answer}</p>
                    </div>
                </div>
            </div>
            """
    
    insights_html = ""
    if isinstance(pack["key_insights"], list):
        for insight in pack["key_insights"]:
            insights_html += f"<li>{insight}</li>\n"
    else:
        insights_html += f"<li>{pack['key_insights']}</li>\n"
    
    questions_html = ""
    if isinstance(pack["questions"], list):
        for i, q in enumerate(pack["questions"], 1):
            questions_html += f"<div class='question-item'><strong>Q{i}:</strong> {q}</div>\n"
    else:
        questions_html += f"<div class='question-item'>{pack['questions']}</div>\n"
    
    action_points_html = ""
    if isinstance(pack["action_points"], list):
        for ap in pack["action_points"]:
            if isinstance(ap, dict):
                action = ap.get("action", "")
                desc = ap.get("description", "")
                action_points_html += f"<div class='action-item'><strong>{action}</strong><p>{desc}</p></div>\n"
            else:
                action_points_html += f"<div class='action-item'>{ap}</div>\n"
    else:
        action_points_html += f"<div class='action-item'>{pack['action_points']}</div>\n"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{pack['filename']} - Summify</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="/static/style.css">
        <style>
            .flashcard {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 12px;
                padding: 24px;
                min-height: 200px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: transform 0.3s;
                user-select: none;
            }}
            .flashcard:hover {{
                transform: scale(1.02);
            }}
            .flashcard p {{
                text-align: center;
                font-size: 18px;
                line-height: 1.6;
            }}
            .question-item, .action-item {{
                background: #f3f4f6;
                padding: 16px;
                border-radius: 8px;
                margin: 12px 0;
                border-left: 4px solid #667eea;
            }}
        </style>
    </head>
    <body class="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white min-h-screen">
        <div class="container mx-auto px-4 py-12">
            <div class="max-w-4xl mx-auto">
                <!-- Header -->
                <div class="mb-12">
                    <a href="/" class="text-purple-400 hover:text-purple-300 mb-4 inline-block">← Back to Summify</a>
                    <h1 class="text-4xl font-bold mb-2">{pack['filename']}</h1>
                    <p class="text-slate-400">Smart Summary Pack • {pack['created_at']}</p>
                </div>
                
                <!-- Summary Section -->
                <section class="mb-12 bg-slate-800 rounded-lg p-8">
                    <h2 class="text-2xl font-bold mb-4 text-purple-400">📋 Summary</h2>
                    <p class="text-slate-200 leading-relaxed">{pack['summary']}</p>
                </section>
                
                <!-- Key Insights Section -->
                <section class="mb-12 bg-slate-800 rounded-lg p-8">
                    <h2 class="text-2xl font-bold mb-6 text-purple-400">💡 Key Insights</h2>
                    <ul class="space-y-3 text-slate-200">
                        {insights_html}
                    </ul>
                </section>
                
                <!-- Flashcards Section -->
                <section class="mb-12 bg-slate-800 rounded-lg p-8">
                    <h2 class="text-2xl font-bold mb-6 text-purple-400">🎓 Flashcards</h2>
                    <p class="text-slate-400 mb-6 text-sm">Click cards to reveal answers</p>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {flashcards_html}
                    </div>
                </section>
                
                <!-- Questions Section -->
                <section class="mb-12 bg-slate-800 rounded-lg p-8">
                    <h2 class="text-2xl font-bold mb-6 text-purple-400">❓ Discussion Questions</h2>
                    <div class="space-y-3">
                        {questions_html}
                    </div>
                </section>
                
                <!-- Action Points Section -->
                <section class="mb-12 bg-slate-800 rounded-lg p-8">
                    <h2 class="text-2xl font-bold mb-6 text-purple-400">🎯 Action Points</h2>
                    <div class="space-y-3">
                        {action_points_html}
                    </div>
                </section>
                
                <!-- Share Section -->
                <section class="mb-12 bg-slate-800 rounded-lg p-8">
                    <h2 class="text-2xl font-bold mb-4 text-purple-400">🔗 Share</h2>
                    <div class="flex gap-4">
                        <input 
                            type="text" 
                            value="{os.getenv('BASE_URL', 'http://localhost:8000')}/pack/{pack_id}/html" 
                            class="flex-1 bg-slate-700 text-white px-4 py-2 rounded border border-slate-600"
                            onclick="this.select()"
                        >
                        <button onclick="copyToClipboard(this)" class="bg-purple-600 hover:bg-purple-700 px-6 py-2 rounded font-semibold">
                            Copy Link
                        </button>
                    </div>
                </section>
                
                <!-- Footer -->
                <footer class="text-center py-8 border-t border-slate-700 mt-12">
                    <p class="text-slate-400 mb-2">Generated with <span class="text-purple-400 font-semibold">Summify</span> — AI Document Intelligence</p>
                    <a href="/" class="text-purple-400 hover:text-purple-300">Create your own smart summary</a>
                </footer>
            </div>
        </div>
        
        <script>
            function copyToClipboard(btn) {{
                const input = btn.previousElementSibling;
                input.select();
                document.execCommand('copy');
                const oldText = btn.textContent;
                btn.textContent = 'Copied!';
                setTimeout(() => {{ btn.textContent = oldText; }}, 2000);
            }}
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Summify"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)