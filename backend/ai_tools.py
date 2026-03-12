import json
import os

# Lazy initialization of Groq client
_client = None
_init_attempted = False

def _get_client():
    """Lazy initialize Groq client - only create when needed."""
    global _client, _init_attempted
    
    if _init_attempted:
        return _client
    
    _init_attempted = True
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        return None
    
    try:
        from groq import Groq
        _client = Groq(api_key=api_key)
        return _client
    except Exception as e:
        print(f"Warning: Could not initialize Groq client: {e}")
        return None

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
    client = _get_client()
    if not client:
        return "This document provides important information and key concepts. The main ideas include critical points that should be understood. Overall, this material covers essential aspects of the topic in detail. Key takeaways are highlighted throughout for easy reference and learning."
    
    prompt = "Provide a clear, concise summary (150-250 words) of the following document:\n\n" + text[:3000] + "\n\nFocus on main ideas and key information. Be direct and informative."
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in summary generation: {e}")
        return "Unable to generate summary at this time."

def _generate_insights(text):
    """Generate key bullet points."""
    client = _get_client()
    if not client:
        return [
            "Core concept clearly explained with examples",
            "Important principle that applies broadly",
            "Critical insight for understanding the topic",
            "Practical application of key ideas",
            "Essential takeaway to remember",
            "Advanced consideration for deeper learning"
        ]
    
    prompt = "Extract 5-7 important key insights or bullet points from this document:\n\n" + text[:3000] + "\n\nFormat as a JSON array of strings. Each point should be a single, clear sentence. Return ONLY valid JSON array, no other text."
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        insights = json.loads(response.choices[0].message.content)
        return insights if isinstance(insights, list) else [str(insights)]
    except Exception as e:
        print(f"Error in insights generation: {e}")
        return ["Unable to generate insights at this time."]

def _generate_flashcards(text):
    client = _get_client()
    if not client:
        return [
            {"question": "What is the main topic discussed?", "answer": "The document covers key concepts and important principles related to the subject matter."},
            {"question": "Why is this important to know?", "answer": "Understanding these concepts helps provide practical knowledge and deeper comprehension of the topic."},
            {"question": "How can this be applied?", "answer": "These principles can be applied in real-world situations to solve problems and improve outcomes."},
            {"question": "What are the core principles?", "answer": "The foundation rests on clear methodology and proven techniques explained in detail."},
            {"question": "What should be remembered most?", "answer": "The key takeaway is that this information provides valuable insights for learning and professional development."}
        ]
    
    prompt = "Create 5 educational flashcards based on this document:\n\n" + text[:3000] + "\n\nReturn as JSON array with objects containing question and answer keys. Return ONLY valid JSON array, no other text."
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600
        )
        
        flashcards = json.loads(response.choices[0].message.content)
        return flashcards if isinstance(flashcards, list) else [flashcards]
    except Exception as e:
        print(f"Error in flashcard generation: {e}")
        return [{"question": "Unable to generate flashcards", "answer": "Please try again"}
    return flashcards if isinstance(flashcards, list) else [flashcards]

def _generate_questions(text):
    """Generate useful questions about the document."""
    if USE_MOCK:
        return [
    client = _get_client()
    if not client:
        return [
            "What is the primary purpose of this document?",
            "How does this relate to common practices?",
            "What would be a practical example of this concept?",
            "What are the limitations or challenges mentioned?",
            "How can someone get started with applying this information?"
        ]
    
    prompt = "Generate 5 thoughtful questions that someone might ask about this document:\n\n" + text[:3000] + "\n\nReturn as JSON array of question strings. Return ONLY valid JSON array, no other text."
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        questions = json.loads(response.choices[0].message.content)
        return questions if isinstance(questions, list) else [str(questions)]
    except Exception as e:
        print(f"Error in questions generation: {e}")
        return ["Unable to generate questions at this time."
    """Generate action points and takeaways."""
    if USE_MOCK:
    client = _get_client()
    if not client:
        return [
            {"action": "Study the Core Concepts", "description": "Review the main principles and ensure understanding of foundational ideas."},
            {"action": "Practice Application", "description": "Work through practical examples to strengthen knowledge and build skills."},
            {"action": "Document Learnings", "description": "Create notes or summaries of key insights for future reference."},
            {"action": "Explore Further", "description": "Research related topics to deepen understanding and expand knowledge."}
        ]
    
    prompt = "Extract 4-5 practical action points or takeaways from this document:\n\n" + text[:3000] + "\n\nReturn as JSON array with objects containing action and description keys. Return ONLY valid JSON array, no other text."
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        actions = json.loads(response.choices[0].message.content)
        return actions if isinstance(actions, list) else [actions]
    except Exception as e:
        print(f"Error in action points generation: {e}")
        return [