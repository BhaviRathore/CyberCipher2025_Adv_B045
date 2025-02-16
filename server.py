from flask import Flask, request, jsonify
import google.generativeai as genai

# Initialize Flask
app = Flask(__name__)

# Set up the AI model (Replace with your actual API key)
API_KEY = "AIzaSyDm82VTUv_D57vwK3E7ZJ3-GBFAaDdlTfs"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

@app.route('/')
def home():
    return "Server is running!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = model.generate_content(user_input)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
