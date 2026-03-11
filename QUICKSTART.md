# 🚀 Quick Start Guide - Summify

## 30 Second Setup

### 1. Get Your OpenAI API Key
- Go to https://platform.openai.com/api_keys
- Click "Create new secret key"
- Copy the key (starts with `sk-`)

### 2. Set the API Key

**On Mac/Linux:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**On Windows (Command Prompt):**
```bash
set OPENAI_API_KEY=sk-your-key-here
```

**On Windows (PowerShell):**
```bash
$env:OPENAI_API_KEY="sk-your-key-here"
```

### 3. Install & Run

**On Mac/Linux:**
```bash
cd /home/gabriel/Desktop/summify
bash start.sh
```

**On Windows:**
```bash
cd \Users\YourUsername\Desktop\summify
start.bat
```

### 4. Open in Browser
Navigate to: **http://localhost:8000**

---

## 🎯 Usage

1. **Upload a PDF** - Click or drag a PDF file
2. **Wait for processing** - Usually 10-30 seconds
3. **View results** - Get summaries, insights, flashcards, questions
4. **Share** - Copy the public link to share with others

---

## 📝 Example Files to Try

### Academic Papers
- Download from ArXiv (arxiv.org)
- Physics, Math, CS papers work great

### Business Documents
- Annual reports
- Case studies  
- Business plans

### Educational Materials
- Textbook chapters (PDF)
- Lecture notes
- Study guides

---

## 🔧 Troubleshooting

**"ModuleNotFoundError: No module named 'fastapi'"**
```bash
pip install -r requirements.txt
```

**"OPENAI_API_KEY not found"**
Make sure you set the environment variable (see Step 2 above)

**"Connection refused on port 8000"**
- Another app is using port 8000
- Or server didn't start - check for errors above

**"PDF processing failed"**
- Try a simpler PDF
- Ensure it's not corrupted
- Try a different PDF

---

## 📚 Learn More

See **README.md** for:
- Full feature list
- API documentation
- Deployment instructions
- Troubleshooting guide

---

## 🎉 Ready to Go!

Your Summify instance is now running locally. Start analyzing PDFs!

**Next steps:**
- [ ] Upload your first PDF
- [ ] Share a summary link with a friend
- [ ] Deploy to production (see README.md)

Happy summarizing! 🎓
