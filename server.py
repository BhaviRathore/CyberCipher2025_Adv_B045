from flask import Flask, render_template, redirect, request, session, url_for, jsonify
import firebase_admin
from firebase_admin import credentials, auth, db
from chatbot import get_ai_response, points_of_log  # Importing the function from chatbot.py


app = Flask(__name__, template_folder="Templates")
app.secret_key = "your_secret_key"  # Required for session handling

# Initialize Firebase Admin SDK
cred = credentials.Certificate("cybercypher-4ca0c-firebase-adminsdk-fbsvc-d64558a934.json")  # Update with your Firebase credentials
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://cybercypher-4ca0c-default-rtdb.asia-southeast1.firebasedatabase.app/"
  # Update with your Firebase DB URL
})

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('loginpage.html')

@app.route('/dashboard')
def dashboard():

    temp = points_of_log()

    if 'user' not in session:
        print("User session not found! Redirecting to login...")
        return redirect(url_for('login'))

    print("User session exists:", session['user'])
    return render_template('dashboard.html', summary = temp, user=session['user'])


@app.route('/verify', methods=['POST'])
def verify():
    id_token = request.json.get('idToken')
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        user_email = decoded_token.get('email', '')

        # Store session
        session['user'] = {'uid': user_id, 'email': user_email}

        # Debugging: Print session
        print("Session set:", session.get('user'))

        # Store session in Firebase DB
        db.reference(f'sessions/{user_id}').set({'email': user_email})

        return jsonify({'success': True, 'message': 'Authentication successful'})
    except Exception as e:
        print("Authentication failed:", str(e))
        return jsonify({'success': False, 'error': str(e)}), 401

@app.route('/chatbot')
def chatbot():
    if 'user' not in session:
        return redirect(url_for('login'))  # Restrict access if not logged in
    return render_template('chatbot.html')
    
@app.route('/get-response', methods=['POST'])
def get_response():
    if 'user' not in session:
        return jsonify({"response": "Please log in first."})

    user_id = session['user']['uid']
    user_message = request.json.get("message")
    
    # Get AI response
    bot_response = get_ai_response(user_message)

    # Store in Firebase
    ref = db.reference(f'chat_history/{user_id}')
    ref.push({"sender": "user", "message": user_message})
    ref.push({"sender": "bot", "message": bot_response})

    return jsonify({"response": bot_response})

@app.route('/get-chat-history', methods=['GET'])
def get_chat_history():
    if 'user' not in session:
        return jsonify([])  # No chat history if user is not logged in

    user_id = session['user']['uid']  # Get the user's Firebase UID
    ref = db.reference(f'chat_history/{user_id}')  # Reference user-specific chat history
    history = ref.get() or {}  # Fetch history, return empty if None

    chat_list = []
    for key, chat in history.items():
        chat_list.append({
            "sender": chat.get("sender", "unknown"),
            "message": chat.get("message", "")
        })

    print("Fetched chat history:", chat_list)  # Debugging log  
    return jsonify(chat_list)  # Return history as JSON


@app.route('/logout')
def logout():
    if 'user' in session:
        user_id = session['user']['uid']
        db.reference(f'sessions/{user_id}').delete()  # Remove session from Firebase DB
        session.pop('user')  # Remove from Flask session

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

