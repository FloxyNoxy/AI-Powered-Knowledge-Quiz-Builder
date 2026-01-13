# **AI Quiz Generator**

A powerful command-line application that automatically generates educational multiple-choice quizzes on any topic using AI. Create, take, and review quizzes with detailed explanations—all from your terminal.

**Features**
 - AI-Powered Generation: Generate quizzes on any topic using Google's Gemini AI

 - Interactive Quiz Taking: Take quizzes with immediate scoring and feedback

 - Detailed Explanations: Learn why answers are correct/incorrect with AI-generated explanations

 - Quiz History: Review past quizzes and results

 - Topic Validation: Smart validation to ensure quiz quality

 - Persistent Storage: All quizzes and results saved automatically

 - Clean CLI Interface: Intuitive, user-friendly command-line interface

**Technologies Used**

Core Framework & Libraries
 - Python 3.10+ - Primary programming language

 - Click - Professional CLI framework for creating beautiful command-line interfaces

 - Google GenAI - Official Google Gemini API client library

 - python-dotenv - Environment variable management

**Architecture & Design**
 - Modular Design - Clean separation of concerns (AI service, storage, quiz engine)

 - Repository Pattern - Abstract data storage layer

 - Data Classes - Type-safe data models with serialization

 - Configuration Management - Centralized config with environment variables

**AI Integration**
 - Google Gemini 2.5 Flash - State-of-the-art language model for quiz generation

 - Structured Output - JSON-based prompt engineering for reliable parsing

 - Two-Stage Validation - Topic validation + quiz generation for quality control

**Why These Technologies?**

Click over alternatives
 - Professional CLI Features: Built-in help, validation, prompts, colors

 - Developer Experience: Decorator-based, less boilerplate than argparse

 - Extensibility: Plugin system, easy to add new commands

 - Testing: Excellent test runner for CLI testing

Google Gemini AI
 - Free Tier: Generous free usage for MVP development

 - Quality: Excellent at following structured JSON prompts

 - Reliability: Google's infrastructure and support

JSON Storage over Database
 - Simplicity: Zero setup, works out of the box

 - Portability: Easy to inspect, backup, and migrate

 - MVP Appropriate: Sufficient for single-user CLI application

 - Future-proof: Easy to replace with SQLite/PostgreSQL later

# Installation
1. Clone the Repository

`git clone https://github.com/FloxyNoxy/AI-Powered-Knowledge-Quiz-Builder.git`

2. Navigate to the project folder

` cd AI-Powered-Knowledge-Quiz-Builder`

3. Install Dependencies

`pip install -r requirements.txt`

# API Key Setup
You need a Google Gemini API key to generate quizzes. Here are three ways to set it up:

# Method 1: .env File
 - Get your API key from Google AI Studio: https://aistudio.google.com/app/api-keys

 - Create .env file in root:

**Linuz/MacOS**: `touch .env`

**Windows**: `type nul > .env`

 - Add your API key to the .env file:

`GEMINI_API_KEY=your_actual_api_key_here`

# Method 2: Environment Variable
Set the API key directly in your shell:

**On macOS/Linux:**

`export GEMINI_API_KEY="your_actual_api_key_here"`

**On Windows (Command Prompt):**

`set GEMINI_API_KEY=your_actual_api_key_here`

**On Windows (PowerShell):**

`$env:GEMINI_API_KEY="your_actual_api_key_here"`

# Verify Setup
Test your API key configuration:

`python test_api.py`

# Quick Start
**Generate Your First Quiz**

`python main.py generate --topic "Ancient Rome"`

**Or simply:**

`python main.py generate`

`python main.py take --quiz-id abc123`

**Or browse recent quizzes**

`python main.py take`

**View History**

`python main.py history`

**Review Results**

`python main.py review`



**View statistics**

`python main.py stats`

**Get help**

`python main.py --help`

`python main.py generate --help`

# Project Structure
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
