import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DATA_FILE = "data/quizzes.json"
    
    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables. "
                           "Please set it in .env file or environment.")