import click
import sys
from datetime import datetime
from quiz_generator import QuizGenerator
from quiz_engine import QuizEngine
from storage import QuizStorage

def print_banner():
    """Print application banner."""
    click.echo("""
    ╔═══════════════════════════════════════════════════════╗
    ║                🤖 AI QUIZ GENERATOR                   ║
    ║        Generate and take quizzes on any topic!        ║
    ╚═══════════════════════════════════════════════════════╝
    """)

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """AI Quiz Generator - Create and take quizzes on any topic!"""
    if ctx.invoked_subcommand is None:
        print_banner()
        click.echo("✨ Available commands:\n")
        click.echo("  📝 generate   - Create a new quiz")
        click.echo("  🎯 take       - Take a quiz")
        click.echo("  📊 history    - View quiz history")
        click.echo("  📖 review     - Review past results")
        click.echo("  📈 stats      - View statistics")
        click.echo("  ❓ help       - Show this help")
        click.echo("\n💡 Try 'quiz generate --topic \"Ancient Rome\"' to get started!")

@cli.command()
@click.option('--topic', prompt='📚 Enter a topic for the quiz', help='Topic for quiz generation')
@click.option('--questions', default=5, help='Number of questions (default: 5)')
def generate(topic, questions):
    """Generate a new quiz on a topic"""
    try:
        click.echo(f"\n🎨 Generating {questions}-question quiz about '{topic}'...")
        
        generator = QuizGenerator()
        quiz = generator.generate_quiz(topic, num_questions=questions)
        
        click.echo(f"✅ Quiz generated successfully!")
        click.echo(f"   📋 ID: {quiz.id}")
        click.echo(f"   📚 Topic: {quiz.topic}")
        click.echo(f"   🔢 Questions: {len(quiz.questions)}")
        click.echo(f"   📅 Created: {quiz.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        click.echo(f"\n🎯 Would you like to take this quiz now?")
        if click.confirm("   Take quiz now?", default=True):
            engine = QuizEngine()
            result = engine.take_quiz(quiz.id)
            if result:
                click.echo(f"\n✅ Quiz completed! Result saved.")
        
    except Exception as e:
        click.echo(f"\n❌ Error: {e}")
        click.echo("💡 Tip: Try a different topic or check your internet connection.")

@cli.command()
@click.option('--quiz-id', help='Specific quiz ID to take')
def take(quiz_id):
    """Take a quiz"""
    engine = QuizEngine()
    storage = QuizStorage()
    generator = QuizGenerator()
    
    if not quiz_id:
        # Show recent quizzes to choose from
        quizzes = storage.get_recent_quizzes(5)
        
        if not quizzes:
            click.echo("\n📭 No quizzes found. Generate one first!")
            click.echo("💡 Try: quiz generate --topic \"Physics\"")
            return
        
        click.echo("\n📚 Recent Quizzes:")
        click.echo("="*60)
        
        for i, quiz in enumerate(quizzes, 1):
            click.echo(f"{i}. {quiz.topic} (ID: {quiz.id}) - {len(quiz.questions)} questions")
        
        click.echo(f"{len(quizzes)+1}. 🔍 Search all quizzes")
        click.echo(f"{len(quizzes)+2}. 🆕 Generate new quiz")
        
        try:
            choice = click.prompt("\nSelect a quiz (number)", type=int)
            
            if 1 <= choice <= len(quizzes):
                quiz_id = quizzes[choice-1].id
            elif choice == len(quizzes) + 1:
                # Show all quizzes
                all_quizzes = storage.get_all_quizzes()
                if not all_quizzes:
                    click.echo("📭 No quizzes found!")
                    return
                
                click.echo("\n📚 All Quizzes:")
                click.echo("="*60)
                for i, quiz in enumerate(all_quizzes, 1):
                    click.echo(f"{i}. {quiz.topic} (ID: {quiz.id})")
                
                sub_choice = click.prompt("\nSelect a quiz (number) or '0' to cancel", type=int)
                if 1 <= sub_choice <= len(all_quizzes[-20:]):
                    quiz_id = all_quizzes[-20:][sub_choice-1].id
                else:
                    click.echo("Returning to main menu...")
                    return
            elif choice == len(quizzes) + 2:
                # Generate new quiz
                topic = click.prompt("📚 Enter topic for new quiz")
                click.echo(f"\n🎨 Generating 5-question quiz about '{topic}'...")
                quiz = generator.generate_quiz(topic, num_questions=5)

                click.echo(f"✅ Quiz generated successfully!")
                click.echo(f"   📋 ID: {quiz.id}")

                # Ask if they want to take it now
                click.echo(f"\n🎯 Would you like to take this quiz now?")
                if click.confirm("   Take quiz now?", default=True):
                    result = engine.take_quiz(quiz.id)
                    if result:
                        click.echo(f"\n✅ Quiz completed! Result saved.")
                return
            else:
                click.echo("❌ Invalid selection!")
                return
                
        except (ValueError, KeyboardInterrupt):
            click.echo("\nReturning to main menu...")
            return
    
    # Take the selected quiz
    result = engine.take_quiz(quiz_id)

@cli.command()
def history():
    """View quiz and result history"""
    storage = QuizStorage()
    
    click.echo("\n📚 QUIZ HISTORY")
    click.echo("="*60)
    
    quizzes = storage.get_recent_quizzes(10)
    if not quizzes:
        click.echo("📭 No quizzes found yet. Generate one with 'quiz generate'!")
        return
    
    click.echo("\n📝 Recent Quizzes:")
    for quiz in quizzes:
        results = storage.get_results_for_quiz(quiz.id)
        best_score = max([r.score for r in results]) if results else 0
        click.echo(f"  • {quiz.topic}")
        click.echo(f"    ID: {quiz.id} | Questions: {len(quiz.questions)}")
        click.echo(f"    Created: {quiz.created_at.strftime('%Y-%m-%d')}")
        if results:
            click.echo(f"    Attempts: {len(results)} | Best: {best_score}/{len(quiz.questions)}")
        click.echo()
    
    # Show recent results
    results = storage.get_all_results()[-5:]  # Last 5 results
    if results:
        click.echo("\n📊 Recent Results:")
        click.echo("-"*40)
        for result in results:
            quiz = storage.get_quiz_by_id(result.quiz_id)
            topic = quiz.topic if quiz else "Unknown"
            click.echo(f"  • {topic}: {result.score}/{result.total_questions}")
            click.echo(f"    Completed: {result.completed_at.strftime('%Y-%m-%d %H:%M')}")
            click.echo()

@cli.command()
@click.option('--result-id', help='Specific result ID to review')
def review(result_id):
    """Review a past quiz with detailed explanations"""
    engine = QuizEngine()
    engine.review_quiz(result_id)

@cli.command()
def stats():
    """View application statistics"""
    storage = QuizStorage()
    stats = storage.get_stats()
    
    click.echo("\n📈 APPLICATION STATISTICS")
    click.echo("="*60)
    
    click.echo(f"\n📚 Quizzes Generated: {stats['total_quizzes']}")
    click.echo(f"📊 Quiz Attempts: {stats['total_results']}")
    click.echo(f"📝 Recent Quizzes: {stats['recent_quizzes']}")
    click.echo(f"🎯 Recent Results: {stats['recent_results']}")
    
    # Calculate average score if we have results
    results = storage.get_all_results()
    if results:
        total_score = sum(r.score for r in results)
        total_possible = sum(r.total_questions for r in results)
        avg_percentage = (total_score / total_possible * 100) if total_possible > 0 else 0
        click.echo(f"\n📊 Average Score: {avg_percentage:.1f}%")
        
        # Find best and worst performances
        best_result = max(results, key=lambda r: r.score/r.total_questions) if results else None
        if best_result:
            quiz = storage.get_quiz_by_id(best_result.quiz_id)
            if quiz:
                percentage = (best_result.score / best_result.total_questions) * 100
                click.echo(f"🏆 Best Performance: {percentage:.1f}% on '{quiz.topic}'")
    
    click.echo(f"\n💾 Data file: {storage.filepath}")
    click.echo(f"📁 Data size: {stats['total_quizzes'] + stats['total_results']} records")

@cli.command()
def help():
    """Show detailed help"""
    print_banner()
    click.echo("""
    📖 COMMAND REFERENCE:
    
    📝 generate [--topic TOPIC] [--questions N]
        Create a new quiz. If no topic is provided, you'll be prompted.
        Example: quiz generate --topic "Space Exploration" --questions 10
    
    🎯 take [--quiz-id ID]
        Take a quiz. If no ID is provided, you can choose from recent quizzes.
        Example: quiz take --quiz-id abc123
    
    📊 history
        View your quiz and result history
    
    📖 review [--result-id ID]
        Review a past quiz with detailed explanations
    
    📈 stats
        View application statistics
    
    ❓ help
        Show this help message
    
    💡 TIPS:
    • Quiz IDs are short 8-character codes shown when you generate a quiz
    • You can review any quiz you've taken to see explanations
    • All data is saved automatically in data/quizzes.json
    
    🎯 EXAMPLE WORKFLOW:
    1. quiz generate --topic "Python Programming"
    2. quiz take (choose the quiz from the list)
    3. quiz review (see your results with explanations)
    """)

if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n\n👋 Goodbye! Thanks for using AI Quiz Generator!")
        sys.exit(0)
    except Exception as e:
        click.echo(f"\n❌ Unexpected error: {e}")
        click.echo("💡 Check your .env file and internet connection, then try again.")
        sys.exit(1)