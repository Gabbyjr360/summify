from groq import Groq
import json
import os

# Use mock AI mode if API key not set
USE_MOCK = not os.getenv("GROQ_API_KEY")

if not USE_MOCK:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
else:
    client = None

def generate_study_material(text):
    """Generate a complete Smart Summary Pack from document text."""
    
    # Generate summary
    summary = _generate_summary(text)
    
    # Generate key insights
    key_insights = _generate_insights(text)
    
    # Generate flashcards
    flashcards = _generate_flashcards(text)
    
    # Generate questions
    questions = _generate_questions(text)
    
    # Generate action points
    action_points = _generate_action_points(text)
    
    return {
        "summary": summary,
        "key_insights": key_insights,
        "flashcards": flashcards,
        "questions": questions,
        "action_points": action_points
    }

def _generate_summary(text):
    """Generate a concise summary."""
    if USE_MOCK:
        return "This document provides important information and key concepts. The main ideas include critical points that should be understood. Overall, this material covers essential aspects of the topic in detail. Key takeaways are highlighted throughout for easy reference and learning."
    
    prompt = "Provide a clear, concise summary (150-250 words) of the following document:\n\n" + text[:3000] + "\n\nFocus on main ideas and key information. Be direct and informative."
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=400
    )
    
    return response.choices[0].message.content

def _generate_insights(text):
    """Generate key bullet points."""
    if USE_MOCK:
        return [
            "Core concept clearly explained with examples",
            "Important principle that applies broadly",
            "Critical insight for understanding the topic",
            "Practical application of key ideas",
            "Essential takeaway to remember",
            "Advanced consideration for deeper learning"
        ]
    
    prompt = "Extract 5-7 important key insights or bullet points from this document:\n\n" + text[:3000] + "\n\nFormat as a JSON array of strings. Each point should be a single, clear sentence. Return ONLY valid JSON array, no other text."
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    try:
        insights = json.loads(response.choices[0].message.content)
    except:
        insights = response.choices[0].message.content.split('\n')
    
    return insights if isinstance(insights, list) else [str(insights)]

def _generate_flashcards(text):
    """Generate learning flashcards."""
    if USE_MOCK:
        return [
            {"question": "What is the main topic discussed?", "answer": "The document covers key concepts and important principles related to the subject matter."},
            {"question": "Why is this important to know?", "answer": "Understanding these concepts helps provide practical knowledge and deeper comprehension of the topic."},
            {"question": "How can this be applied?", "answer": "These principles can be applied in real-world situations to solve problems and improve outcomes."},
            {"question": "What are the core principles?", "answer": "The foundation rests on clear methodology and proven techniques explained in detail."},
            {"question": "What should be remembered most?", "answer": "The key takeaway is that this information provides valuable insights for learning and professional development."}
        ]
    
    prompt = "Create 5 educational flashcards based on this document:\n\n" + text[:3000] + "\n\nReturn as JSON array with objects containing question and answer keys. Return ONLY valid JSON array, no other text."
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=600
    )
    
    try:
        flashcards = json.loads(response.choices[0].message.content)
    except:
        flashcards = [
            {"question": "What is the main topic?", "answer": "See summary above"},
            {"question": "What are key points?", "answer": "See insights above"}
        ]
    
    return flashcards if isinstance(flashcards, list) else [flashcards]

def _generate_questions(text):
    """Generate useful questions about the document."""
    if USE_MOCK:
        return [
            "What is the primary purpose of this document?",
            "How does this relate to common practices?",
            "What would be a practical example of this concept?",
            "What are the limitations or challenges mentioned?",
            "How can someone get started with applying this information?"
        ]
    
    prompt = "Generate 5 thoughtful questions that someone might ask about this document:\n\n" + text[:3000] + "\n\nReturn as JSON array of question strings. Return ONLY valid JSON array, no other text."
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    try:
        questions = json.loads(response.choices[0].message.content)
    except:
        questions = response.choices[0].message.content.split('\n')
    
    return questions if isinstance(questions, list) else [str(questions)]

def _generate_action_points(text):
    """Generate action points and takeaways."""
    if USE_MOCK:
        return [
            {"action": "Study the Core Concepts", "description": "Review the main principles and ensure understanding of foundational ideas."},
            {"action": "Practice Application", "description": "Work through practical examples to strengthen knowledge and build skills."},
            {"action": "Document Learnings", "description": "Create notes or summaries of key insights for future reference."},
            {"action": "Explore Further", "description": "Research related topics to deepen understanding and expand knowledge."}
        ]
    
    prompt = "Extract 4-5 practical action points or takeaways from this document:\n\n" + text[:3000] + "\n\nReturn as JSON array with objects containing action and description keys. Return ONLY valid JSON array, no other text."
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    try:
        actions = json.loads(response.choices[0].message.content)
    except:
        actions = []
    
    return actions if isinstance(actions, list) else [actions]