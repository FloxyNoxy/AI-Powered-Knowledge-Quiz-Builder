import google.genai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"Testing API key: {api_key[:10]}...")

try:
    client = genai.Client(api_key=api_key)
    
    # Test with a simple prompt
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello in one word."
    )
    
    print(f"Success! Response: {response.text}")
    print("API key is working correctly!")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nTroubleshooting steps:")
    print("1. Check your .env file has GEMINI_API_KEY=your_key_here")
    print("2. Make sure you installed google-genai: pip install google-genai")
    print("3. Verify your API key is valid at https://aistudio.google.com/app/apikey")
    print("4. Check your internet connection")