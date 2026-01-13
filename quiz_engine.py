import click
from datetime import datetime
from typing import Optional, Tuple
from models import Quiz, QuizResult
from storage import QuizStorage

class QuizEngine:
    def __init__(self):
        self.storage = QuizStorage()
    
    def take_quiz(self, quiz_id: str) -> Optional[QuizResult]:
        """Take a quiz interactively and return the result."""
        quiz = self.storage.get_quiz_by_id(quiz_id)
        
        if not quiz:
            click.echo(f"❌ Quiz with ID '{quiz_id}' not found!")
            return None
        
        click.echo(f"\n{'='*60}")
        click.echo(f"📝 QUIZ: {quiz.topic}")
        click.echo(f"📅 Created: {quiz.created_at.strftime('%Y-%m-%d %H:%M')}")
        click.echo(f"🔢 Questions: {len(quiz.questions)}")
        click.echo(f"{'='*60}\n")
        
        user_answers = []
        
        # Ask each question
        for i, question in enumerate(quiz.questions, 1):
            click.echo(f"\nQuestion {i}/{len(quiz.questions)}")
            click.echo(f"{'─'*40}")
            click.echo(f"❓ {question.question_text}")
            click.echo()
            
            # Display options
            for j, option in enumerate(question.options):
                click.echo(f"   {chr(65+j)}) {option}")
            
            # Get user's answer
            while True:
                try:
                    answer_input = click.prompt(f"\nYour answer (A/B/C/D)", type=str).upper().strip()
                    if answer_input in ['A', 'B', 'C', 'D']:
                        answer_index = ord(answer_input) - 65  # A=0, B=1, etc.
                        user_answers.append(answer_index)
                        break
                    else:
                        click.echo("❌ Please enter only A, B, C, or D")
                except (KeyboardInterrupt, EOFError):
                    click.echo("\n\n⚠️ Quiz cancelled!")
                    return None
        
        # Calculate score
        correct_answers = 0
        for i, question in enumerate(quiz.questions):
            if user_answers[i] == question.correct_index:
                correct_answers += 1
        
        # Create result
        result = QuizResult(
            quiz_id=quiz_id,
            user_answers=user_answers,
            score=correct_answers,
            total_questions=len(quiz.questions),
            completed_at=datetime.now()
        )
        
        # Save result
        self.storage.save_result(result)
        
        # Display results
        self._display_results(quiz, result)
        
        return result
    
    def review_quiz(self, result_id: Optional[str] = None):
        """Review a specific quiz result or let user choose one."""
        results = self.storage.get_all_results()
        
        if not results:
            click.echo("📭 No quiz results found. Take a quiz first!")
            return
        
        if result_id:
            # Find specific result
            result = next((r for r in results if r.quiz_id == result_id), None)
            if not result:
                click.echo(f"❌ Result with ID '{result_id}' not found!")
                return
            
            quiz = self.storage.get_quiz_by_id(result.quiz_id)
            if quiz:
                self._display_detailed_review(quiz, result)
            else:
                click.echo(f"❌ Quiz for result '{result_id}' not found!")
        else:
            # Let user choose from recent results
            click.echo("\n📊 Recent Quiz Results:")
            click.echo("="*60)
            
            recent_results = results[-10:]  # Last 10 results
            for i, result in enumerate(recent_results, 1):
                quiz = self.storage.get_quiz_by_id(result.quiz_id)
                topic = quiz.topic if quiz else "Unknown Topic"
                click.echo(f"{i}. {topic} - Score: {result.score}/{result.total_questions} "
                          f"({result.completed_at.strftime('%Y-%m-%d')})")
            
            try:
                choice = click.prompt("\nSelect a result to review (number) or 'q' to quit", type=str)
                if choice.lower() != 'q':
                    idx = int(choice) - 1
                    if 0 <= idx < len(recent_results):
                        quiz = self.storage.get_quiz_by_id(recent_results[idx].quiz_id)
                        if quiz:
                            self._display_detailed_review(quiz, recent_results[idx])
                        else:
                            click.echo("❌ Could not find the quiz for this result!")
                    else:
                        click.echo("❌ Invalid selection!")
            except (ValueError, KeyboardInterrupt):
                click.echo("\nReturning to main menu...")
    
    def _display_results(self, quiz: Quiz, result: QuizResult):
        """Display quiz results with explanations."""
        click.echo(f"\n{'='*60}")
        click.echo("📊 QUIZ RESULTS")
        click.echo(f"{'='*60}")
        
        percentage = (result.score / result.total_questions) * 100
        click.echo(f"\n🎯 Your Score: {result.score}/{result.total_questions} ({percentage:.1f}%)")
        
        if percentage >= 80:
            click.echo("🌟 Excellent work!")
        elif percentage >= 60:
            click.echo("👍 Good job!")
        else:
            click.echo("📚 Keep learning!")
        
        click.echo(f"\n⏰ Completed: {result.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Ask if user wants to review answers
        if click.confirm("\n📖 Would you like to review the answers with explanations?", default=True):
            self._display_detailed_review(quiz, result)
    
    def _display_detailed_review(self, quiz: Quiz, result: QuizResult):
        """Display detailed review of each question with explanations."""
        click.echo(f"\n{'='*60}")
        click.echo(f"📖 DETAILED REVIEW: {quiz.topic}")
        click.echo(f"{'='*60}")
        
        for i, (question, user_answer) in enumerate(zip(quiz.questions, result.user_answers), 1):
            is_correct = user_answer == question.correct_index
            status = "✅ CORRECT" if is_correct else "❌ INCORRECT"
            
            click.echo(f"\nQ{i}: {status}")
            click.echo(f"❓ {question.question_text}")
            
            # Show all options with indicators
            for j, option in enumerate(question.options):
                prefix = ""
                if j == question.correct_index:
                    prefix = "✓ "  # Correct answer
                elif j == user_answer and not is_correct:
                    prefix = "✗ "  # User's wrong answer
                
                click.echo(f"   {chr(65+j)}) {prefix}{option}")
            
            click.echo(f"\n💡 Explanation: {question.explanation}")
            click.echo("-"*40)