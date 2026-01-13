from dataclasses import dataclass, asdict
from typing import List
from datetime import datetime
import uuid

@dataclass
class Question:
    question_text: str
    options: List[str]  # 4 options
    correct_index: int  # 0-3
    explanation: str    # Why this answer is correct
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            question_text=data["question_text"],
            options=data["options"],
            correct_index=data["correct_index"],
            explanation=data["explanation"]
        )

@dataclass
class Quiz:
    id: str
    topic: str
    questions: List[Question]
    created_at: datetime
    
    def to_dict(self):
        return {
            "id": self.id,
            "topic": self.topic,
            "questions": [q.to_dict() for q in self.questions],
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            topic=data["topic"],
            questions=[Question.from_dict(q) for q in data["questions"]],
            created_at=datetime.fromisoformat(data["created_at"])
        )

@dataclass
class QuizResult:
    quiz_id: str
    user_answers: List[int]  # indices of user's choices
    score: int
    total_questions: int
    completed_at: datetime
    
    def to_dict(self):
        return {
            "quiz_id": self.quiz_id,
            "user_answers": self.user_answers,
            "score": self.score,
            "total_questions": self.total_questions,
            "completed_at": self.completed_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            quiz_id=data["quiz_id"],
            user_answers=data["user_answers"],
            score=data["score"],
            total_questions=data["total_questions"],
            completed_at=datetime.fromisoformat(data["completed_at"])
        )