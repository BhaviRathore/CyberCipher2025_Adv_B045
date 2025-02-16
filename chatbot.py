import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

# Get API key from .env
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the client with the API key
client = genai.Client(api_key=api_key)

def get_ai_response(user_input):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=user_input
        )
        return response.text
    except Exception as e:
        return "Error: Unable to generate response."
