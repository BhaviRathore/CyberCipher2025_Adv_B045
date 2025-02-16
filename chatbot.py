import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

# Get API key from .env
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the client with the API key
client = genai.Client(api_key=api_key)

# Make a request
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works"
)

print(response.text)
