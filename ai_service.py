import google.genai as genai
import json
import re
from typing import List
from models import Question

class AIService:
    def __init__(self, api_key: str):
        # Configure with the new API
        self.client = genai.Client(api_key=api_key)

    def validate_topic(self, topic: str) -> tuple[bool, str]:
        """Validate if a topic is appropriate for quiz generation.
        Returns (is_valid, message)"""
        
        prompt = f"""Evaluate if this topic is appropriate for creating educational multiple-choice questions: "{topic}"

        Consider:
        1. Is it a coherent, meaningful topic?
        2. Is it educational/appropriate?
        3. Is it not gibberish, random characters, or nonsense?

        Return a JSON response with:
        - "valid": true/false
        - "reason": brief explanation
        - "suggestion": alternative topic if invalid (or null if valid)

        Example valid response:
        {{"valid": true, "reason": "Topic is clear and educational", "suggestion": null}}

        Example invalid response:
        {{"valid": false, "reason": "Appears to be random characters", "suggestion": "Try 'Ancient History' or 'Computer Science'"}}"""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            # Parse response
            result = json.loads(self._extract_json(response.text))
            
            return result.get("valid", False), result.get("reason", "Unknown error")
            
        except Exception as e:
            # If validation fails, be conservative but allow
            print(f"Warning: Topic validation failed: {e}")
            return True, "Validation skipped"
        
    def generate_quiz_questions(self, topic: str, num_questions: int = 5) -> List[Question]:
        prompt = f"""You are an expert quiz creator. Generate {num_questions} high-quality multiple-choice questions about "{topic}".

        For EACH question, you MUST provide:
        1. "question_text": The question text
        2. "options": A list of EXACTLY 4 options (as strings)
        3. "correct_index": The index of the correct option (0 for first option, 1 for second, etc.)
        4. "explanation": A clear explanation of why the correct answer is right (1-2 sentences)

        IMPORTANT RULES:
        - Questions should be diverse and cover different aspects of "{topic}"
        - Make incorrect options plausible but clearly wrong to someone who knows the topic
        - Ensure correct_index is always 0, 1, 2, or 3
        - Keep explanations educational and concise
        
        Return ONLY a valid JSON array. No additional text before or after.

        Example format:
        [
          {{
            "question_text": "What is the capital of France?",
            "options": ["Berlin", "Madrid", "Paris", "Rome"],
            "correct_index": 2,
            "explanation": "Paris is the capital of France, while Berlin is Germany's capital, Madrid is Spain's, and Rome is Italy's."
          }}
        ]

        Now generate {num_questions} questions about "{topic}":"""
        
        try:
            print(f"Generating {num_questions} questions about '{topic}' via Gemini API...")
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            response_text = response.text
            
            # Clean and extract JSON
            json_str = self._extract_json(response_text)
            
            # Parse JSON
            questions_data = json.loads(json_str)
            
            # Validate and create Question objects
            questions = []
            for i, q_data in enumerate(questions_data[:num_questions]):
                # Validate the question has all required fields
                if not all(k in q_data for k in ["question_text", "options", "correct_index", "explanation"]):
                    print(f"Warning: Question {i+1} missing required fields, skipping")
                    continue
                
                # Ensure we have exactly 4 options
                if len(q_data["options"]) != 4:
                    print(f"Warning: Question {i+1} doesn't have 4 options, skipping")
                    continue
                
                # Ensure correct_index is valid
                if not 0 <= q_data["correct_index"] <= 3:
                    print(f"Warning: Question {i+1} has invalid correct_index, skipping")
                    continue
                
                questions.append(Question(
                    question_text=q_data["question_text"].strip(),
                    options=[opt.strip() for opt in q_data["options"]],
                    correct_index=q_data["correct_index"],
                    explanation=q_data["explanation"].strip()
                ))
            
            # Ensure we have at least some questions
            if not questions:
                raise ValueError("No valid questions were generated. Please try again with a different topic.")
            
            print(f"Successfully generated {len(questions)} questions")
            return questions
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print("Raw response:", response_text[:500] if 'response_text' in locals() else "No response")
            raise Exception(f"Failed to parse AI response as JSON. The AI might not have followed instructions.")
        except Exception as e:
            print(f"Error in AI service: {e}")
            raise Exception(f"Failed to generate quiz: {str(e)}")
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from the AI response, handling various formats."""
        if not text:
            return "[]"
            
        # Remove markdown code blocks
        text = text.replace('```json', '').replace('```', '')
        
        # Find the first [ and last ]
        start = text.find('[')
        end = text.rfind(']') + 1
        
        if start != -1 and end != 0:
            json_str = text[start:end]
            # Try to fix common JSON issues
            json_str = json_str.replace('\n', ' ').replace('\r', ' ')
            # Remove trailing commas before closing brackets
            json_str = re.sub(r',\s*([\]}])', r'\1', json_str)
            return json_str
        
        # If no brackets found, try to find JSON object
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end != 0:
            return text[start:end]
        
        # Return cleaned text as last resort
        return text.strip()