import uuid
from datetime import datetime
from config import Config
from ai_service import AIService
from models import Quiz, Question
from storage import QuizStorage
import re

class QuizGenerator:
    def __init__(self):
        Config.validate()
        self.ai_service = AIService(Config.GEMINI_API_KEY)
        self.storage = QuizStorage()
    
    def generate_quiz(self, topic: str, num_questions: int = 5) -> Quiz:
        """Generate a new quiz on the given topic."""

        # Basic topic validation
        if not topic or not topic.strip():
            raise ValueError("Topic cannot be empty")
        
        if num_questions < 1 or num_questions > 20:
            raise ValueError("Number of questions must be between 1 and 20")

        if len(topic) < 2:
            raise ValueError("Topic must be at least 2 characters long")
    
        if len(topic) > 100:
            raise ValueError("Topic is too long (max 100 characters)")

        #AI-powered topic validation
        print("🤔 Validating topic...")
        is_valid, reason = self.ai_service.validate_topic(topic)

        if not is_valid:
            raise ValueError(f"Topic '{topic}' is not suitable for a quiz. {reason}")
        # Generate questions using AI
        questions = self.ai_service.generate_quiz_questions(topic, num_questions)
        
        # Create quiz
        quiz = Quiz(
            id=str(uuid.uuid4())[:8],  # Short ID for easier reference
            topic=topic,
            questions=questions,
            created_at=datetime.now()
        )
        
        # Save to storage
        self.storage.save_quiz(quiz)
        
        return quiz