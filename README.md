AI Quiz Generator
A powerful command-line application that automatically generates educational multiple-choice quizzes on any topic using AI. Create, take, and review quizzes with detailed explanations—all from your terminal.

Features
AI-Powered Generation: Generate quizzes on any topic using Google's Gemini AI

Interactive Quiz Taking: Take quizzes with immediate scoring and feedback

Detailed Explanations: Learn why answers are correct/incorrect with AI-generated explanations

Quiz History: Review past quizzes and results

Topic Validation: Smart validation to ensure quiz quality

Persistent Storage: All quizzes and results saved automatically

Clean CLI Interface: Intuitive, user-friendly command-line interface

Technologies Used
Core Framework & Libraries
Python 3.10+ - Primary programming language

Click - Professional CLI framework for creating beautiful command-line interfaces

Google GenAI - Official Google Gemini API client library

python-dotenv - Environment variable management

Architecture & Design
Modular Design - Clean separation of concerns (AI service, storage, quiz engine)

Repository Pattern - Abstract data storage layer

Data Classes - Type-safe data models with serialization

Configuration Management - Centralized config with environment variables

AI Integration
Google Gemini 2.5 Flash - State-of-the-art language model for quiz generation

Structured Output - JSON-based prompt engineering for reliable parsing

Two-Stage Validation - Topic validation + quiz generation for quality control

Why These Technologies?
Python
Ecosystem: Rich libraries for AI/ML, data processing, and CLI development

Productivity: Rapid prototyping perfect for 2-day MVP constraint

Team Skills: Widely known, easier for team collaboration and hiring

Click over alternatives
Professional CLI Features: Built-in help, validation, prompts, colors

Developer Experience: Decorator-based, less boilerplate than argparse

Extensibility: Plugin system, easy to add new commands

Testing: Excellent test runner for CLI testing

Google Gemini AI
Free Tier: Generous free usage for MVP development

Quality: Excellent at following structured JSON prompts

Reliability: Google's infrastructure and support

Python SDK: Well-designed, actively maintained client library

JSON Storage over Database
Simplicity: Zero setup, works out of the box

Portability: Easy to inspect, backup, and migrate

MVP Appropriate: Sufficient for single-user CLI application

Future-proof: Easy to replace with SQLite/PostgreSQL later

Installation
1. Clone the Repository
bash
git clone https://github.com/yourusername/ai-quiz-generator.git
cd ai-quiz-generator
2. Create Virtual Environment (Recommended)
bash
# Using venv
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
3. Install Dependencies
bash
pip install -r requirements.txt

API Key Setup
You need a Google Gemini API key to generate quizzes. Here are three ways to set it up:

Method 1: .env File (Recommended)
Get your API key from Google AI Studio

Create a .env file in the project root:

bash
touch .env
Add your API key to the .env file:

text
GEMINI_API_KEY=your_actual_api_key_here
Method 2: Environment Variable
Set the API key directly in your shell:

bash
# On macOS/Linux:
export GEMINI_API_KEY="your_actual_api_key_here"

# On Windows (Command Prompt):
set GEMINI_API_KEY=your_actual_api_key_here

# On Windows (PowerShell):
$env:GEMINI_API_KEY="your_actual_api_key_here"

Verify Setup
Test your API key configuration:

bash
python test_api.py

Quick Start
Generate Your First Quiz
bash
python main.py generate --topic "Ancient Rome"
Or simply:

bash
python main.py generate
# You'll be prompted for a topic
Take a Quiz
bash
# Take a specific quiz by ID
python main.py take --quiz-id abc123

# Or browse recent quizzes
python main.py take
View History
bash
python main.py history
Review Results
bash
python main.py review

Usage Examples
Basic Workflow
bash
# 1. Generate a quiz
python main.py generate --topic "Python Programming" --questions 10

# 2. Take the quiz (note the ID from generation)
python main.py take --quiz-id 8a3b2c1d

# 3. Review your results
python main.py review
Advanced Usage
bash
# Generate without taking immediately
python main.py generate --topic "Quantum Physics" --no-take

# View statistics
python main.py stats

# Get help
python main.py --help
python main.py generate --help

Project Structure
text
ai-quiz-generator/
├── main.py              # CLI entry point with Click commands
├── config.py            # Configuration and environment setup
├── models.py            # Data models (Quiz, Question, QuizResult)
├── ai_service.py        # Gemini AI integration and prompt engineering
├── quiz_generator.py    # Quiz generation orchestration
├── quiz_engine.py       # Quiz taking and scoring logic
├── storage.py           # JSON-based data persistence
├── test_api.py          # API connectivity test
├── .env                 # Environment variables (create this)
├── data/                # Auto-created: stores quizzes.json
├── requirements.txt     # Python dependencies
└── README.md 