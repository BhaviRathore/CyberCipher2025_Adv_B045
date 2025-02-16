import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

# Get API key from .env
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the client with the API key
client = genai.Client(api_key=api_key)

LOG_FILE = "log.txt"  # File to store conversation history

def summarize_log():
    """Summarizes the log file when it gets too long."""
    try:
        with open(LOG_FILE, "r") as file:
            conversation = file.read()

        if len(conversation.split()) > 1000:  # Summarize if log is too long
            summary_prompt = f"Summarize this conversation concisely:\n{conversation}\nSummary:"
            summary_response = client.models.generate_content(
                model="gemini-2.0-flash", contents=summary_prompt
            )
            summary = summary_response.text.strip()

            with open(LOG_FILE, "w") as file:
                file.write(summary + "\n\n")  # Replace with summary

    except FileNotFoundError:
        pass  # No log file yet, so nothing to summarize

def get_ai_response(user_input):
    """Generates AI response while maintaining conversation history."""
    try:
        # Read conversation history
        try:
            with open(LOG_FILE, "r") as file:
                conversation_history = file.read()
        except FileNotFoundError:
            conversation_history = ""

        # Create prompt with past history
        prompt = f"Here is the conversation history:\n{conversation_history}\nUser: {user_input}\nAI:"

        # Generate AI response
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        ai_response = response.text.strip()

        # Append new conversation to log
        with open(LOG_FILE, "a") as file:
            file.write(f"User: {user_input}\nAI: {ai_response}\n\n")

        # Summarize log if necessary
        summarize_log()

        return ai_response

    except Exception as e:
        return "Error: Unable to generate response."

