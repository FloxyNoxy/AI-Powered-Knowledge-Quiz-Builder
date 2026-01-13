import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from models import Quiz, QuizResult

class QuizStorage:
    def __init__(self, filepath: str = "data/quizzes.json"):
        self.filepath = filepath
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Create directory and file if they don't exist."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            initial_data = {
                "quizzes": [],
                "results": [],
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "total_quizzes": 0,
                    "total_results": 0
                }
            }
            self._save_data(initial_data)
    
    def save_quiz(self, quiz: Quiz) -> bool:
        """Save a quiz to storage."""
        try:
            data = self._load_data()
            data["quizzes"].append(quiz.to_dict())
            data["metadata"]["total_quizzes"] = len(data["quizzes"])
            self._save_data(data)
            return True
        except Exception as e:
            print(f"Error saving quiz: {e}")
            return False
    
    def save_result(self, result: QuizResult) -> bool:
        """Save a quiz result to storage."""
        try:
            data = self._load_data()
            data["results"].append(result.to_dict())
            data["metadata"]["total_results"] = len(data["results"])
            self._save_data(data)
            return True
        except Exception as e:
            print(f"Error saving result: {e}")
            return False
    
    def get_quiz_by_id(self, quiz_id: str) -> Optional[Quiz]:
        """Get a specific quiz by ID."""
        data = self._load_data()
        for quiz_dict in data["quizzes"]:
            if quiz_dict["id"] == quiz_id:
                return Quiz.from_dict(quiz_dict)
        return None
    
    def get_all_quizzes(self) -> List[Quiz]:
        """Get all quizzes."""
        data = self._load_data()
        return [Quiz.from_dict(q) for q in data["quizzes"]]
    
    def get_recent_quizzes(self, limit: int = 10) -> List[Quiz]:
        """Get most recent quizzes."""
        data = self._load_data()
        quizzes = [Quiz.from_dict(q) for q in data["quizzes"][-limit:]]
        return quizzes
    
    def get_all_results(self) -> List[QuizResult]:
        """Get all quiz results."""
        data = self._load_data()
        return [QuizResult.from_dict(r) for r in data["results"]]
    
    def get_results_for_quiz(self, quiz_id: str) -> List[QuizResult]:
        """Get all results for a specific quiz."""
        data = self._load_data()
        return [QuizResult.from_dict(r) for r in data["results"] if r["quiz_id"] == quiz_id]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        data = self._load_data()
        return {
            "total_quizzes": len(data["quizzes"]),
            "total_results": len(data["results"]),
            "recent_quizzes": len(data["quizzes"][-5:]),
            "recent_results": len(data["results"][-5:])
        }
    
    def _load_data(self) -> Dict[str, Any]:
        """Load data from JSON file."""
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file is corrupted, reinitialize
            self._ensure_directory()
            with open(self.filepath, 'r') as f:
                return json.load(f)
    
    def _save_data(self, data: Dict[str, Any]):
        """Save data to JSON file."""
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)