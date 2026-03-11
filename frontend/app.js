// Utility Functions
const API_BASE = window.location.origin;

function scrollToUpload() {
    document.getElementById('upload').scrollIntoView({ behavior: 'smooth' });
}

function showLoading() {
    document.getElementById('loadingState').classList.remove('hidden');
    document.getElementById('resultSection').classList.add('hidden');
    document.getElementById('errorState').classList.add('hidden');
}

function hideLoading() {
    document.getElementById('loadingState').classList.add('hidden');
}

function showError(message) {
    document.getElementById('errorState').textContent = message;
    document.getElementById('errorState').classList.remove('hidden');
    document.getElementById('resultSection').classList.add('hidden');
}

function showResult(data) {
    document.getElementById('resultSection').classList.remove('hidden');
    document.getElementById('errorState').classList.add('hidden');
    
    const resultContent = document.getElementById('resultContent');
    const packId = data.pack_id;
    const result = data.result;
    
    let flashcardsHtml = '';
    if (Array.isArray(result.flashcards)) {
        result.flashcards.forEach((card, index) => {
            const question = typeof card === 'object' ? card.question : card;
            const answer = typeof card === 'object' ? card.answer : '';
            
            flashcardsHtml += `
                <div class="flashcard" onclick="this.classList.toggle('flipped')" data-index="${index}">
                    <div class="flashcard-inner">
                        <div class="flashcard-front">
                            <p>${question}</p>
                        </div>
                        <div class="flashcard-back">
                            <p>${answer}</p>
                        </div>
                    </div>
                </div>
            `;
        });
    }
    
    let insightsHtml = '';
    if (Array.isArray(result.key_insights)) {
        result.key_insights.forEach(insight => {
            insightsHtml += `<li>${insight}</li>`;
        });
    }
    
    let questionsHtml = '';
    if (Array.isArray(result.questions)) {
        result.questions.forEach((q, i) => {
            questionsHtml += `<div class='question-item'><strong>Q${i + 1}:</strong> ${q}</div>`;
        });
    }
    
    let actionPointsHtml = '';
    if (Array.isArray(result.action_points)) {
        result.action_points.forEach(ap => {
            if (typeof ap === 'object') {
                actionPointsHtml += `<div class='action-item'><strong>${ap.action}</strong><p>${ap.description}</p></div>`;
            } else {
                actionPointsHtml += `<div class='action-item'>${ap}</div>`;
            }
        });
    }
    
    const shareUrl = `${API_BASE}/pack/${packId}/html`;
    
    resultContent.innerHTML = `
        <div class="space-y-8">
            <!-- Summary Section -->
            <div class="bg-slate-700/50 rounded-lg p-8">
                <h3 class="text-2xl font-bold mb-4 text-purple-400">📋 Summary</h3>
                <p class="text-slate-200 leading-relaxed">${result.summary}</p>
            </div>
            
            <!-- Key Insights Section -->
            <div class="bg-slate-700/50 rounded-lg p-8">
                <h3 class="text-2xl font-bold mb-4 text-purple-400">💡 Key Insights</h3>
                <ul class="space-y-2 text-slate-200 list-disc list-inside">
                    ${insightsHtml}
                </ul>
            </div>
            
            <!-- Flashcards Section -->
            <div class="bg-slate-700/50 rounded-lg p-8">
                <h3 class="text-2xl font-bold mb-4 text-purple-400">🎓 Flashcards</h3>
                <p class="text-slate-400 text-sm mb-6">Click cards to reveal answers</p>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    ${flashcardsHtml}
                </div>
            </div>
            
            <!-- Questions Section -->
            <div class="bg-slate-700/50 rounded-lg p-8">
                <h3 class="text-2xl font-bold mb-4 text-purple-400">❓ Discussion Questions</h3>
                <div class="space-y-3">
                    ${questionsHtml}
                </div>
            </div>
            
            <!-- Action Points Section -->
            <div class="bg-slate-700/50 rounded-lg p-8">
                <h3 class="text-2xl font-bold mb-4 text-purple-400">🎯 Action Points</h3>
                <div class="space-y-3">
                    ${actionPointsHtml}
                </div>
            </div>
            
            <!-- Share Section -->
            <div class="bg-slate-700/50 rounded-lg p-8">
                <h3 class="text-2xl font-bold mb-4 text-purple-400">🔗 Share Your Smart Summary Pack</h3>
                <div class="flex gap-2 flex-col sm:flex-row">
                    <input 
                        type="text" 
                        value="${shareUrl}" 
                        class="flex-1 bg-slate-600 text-white px-4 py-3 rounded border border-slate-500" 
                        onclick="this.select(); document.execCommand('copy')"
                        readonly
                    >
                    <button onclick="copyShareLink('${shareUrl}')" class="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded font-semibold transition whitespace-nowrap">
                        📋 Copy
                    </button>
                    <a href="${shareUrl}" target="_blank" class="bg-pink-600 hover:bg-pink-700 px-6 py-3 rounded font-semibold transition whitespace-nowrap text-center">
                        🔗 View Public
                    </a>
                </div>
                <p class="text-slate-400 text-sm mt-3">Share this link with others to view your summary!</p>
            </div>
            
            <!-- New Upload -->
            <div class="text-center">
                <button onclick="resetUpload()" class="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 px-8 py-3 rounded-lg font-semibold transition">
                    ✨ Analyze Another PDF
                </button>
            </div>
        </div>
    `;
}

function copyShareLink(url) {
    navigator.clipboard.writeText(url).then(() => {
        alert('Link copied to clipboard!');
    });
}

function resetUpload() {
    document.getElementById('fileInput').value = '';
    document.getElementById('resultSection').classList.add('hidden');
    document.getElementById('errorState').classList.add('hidden');
    document.getElementById('loadingState').classList.add('hidden');
    scrollToUpload();
}

// Drag and Drop Handlers
const dropZone = document.getElementById('dropZone');

function handleDragOver(e) {
    e.preventDefault();
    dropZone.style.borderColor = '#a78bfa';
    dropZone.style.backgroundColor = 'rgba(168, 85, 247, 0.1)';
}

function handleDragLeave(e) {
    dropZone.style.borderColor = '#475569';
    dropZone.style.backgroundColor = '';
}

function handleDrop(e) {
    e.preventDefault();
    dropZone.style.borderColor = '#475569';
    dropZone.style.backgroundColor = '';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        document.getElementById('fileInput').files = files;
        handleFileSelect({ target: document.getElementById('fileInput') });
    }
}

// File Upload Handler
async function handleFileSelect(e) {
    const file = e.target.files[0];
    
    if (!file) return;
    
    if (!file.name.endsWith('.pdf')) {
        showError('❌ Please upload a PDF file');
        return;
    }
    
    if (file.size > 50 * 1024 * 1024) {
        showError('❌ File size must be less than 50MB');
        return;
    }
    
    showLoading();
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to analyze document');
        }
        
        const data = await response.json();
        
        if (data.success) {
            hideLoading();
            showResult(data);
        } else {
            throw new Error(data.message || 'Analysis failed');
        }
    } catch (error) {
        hideLoading();
        showError(`❌ Error: ${error.message}`);
        console.error('Upload error:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Summify initialized');
});