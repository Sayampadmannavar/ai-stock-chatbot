import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

AIML_API_KEY = os.getenv("AIML_API_KEY")

if not AIML_API_KEY:
    raise ValueError("❌ AIML_API_KEY not found in .env")

# Initialize AIML API client
client = OpenAI(
    api_key=AIML_API_KEY,
    base_url="https://api.aimlapi.com/v1"  # AIML API endpoint
)

def ask_ai(prompt: str) -> str:
    """
    Sends a user prompt to AIML API and returns the AI response.
    """
    try:
        response = client.chat.completions.create(
            model="openai/gpt-5-2",  # ✅ Correct model for AIML API
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional financial stock market assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500
        )

        # Return the AI's message
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ AIML API Error: {str(e)}"
