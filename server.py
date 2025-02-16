from flask import Flask, render_template, redirect, request, session, url_for, jsonify
import firebase_admin
from firebase_admin import credentials, auth, db

app = Flask(__name__, template_folder="Templates")
app.secret_key = "your_secret_key"  # Required for session handling

# Initialize Firebase Admin SDK
cred = credentials.Certificate("cybercypher-4ca0c-firebase-adminsdk-fbsvc-d64558a934.json")  # Update with your Firebase credentials
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://your-database-url.firebaseio.com"
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
    # Redirect to login if not authenticated
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html', user=session['user'])

@app.route('/verify', methods=['POST'])
def verify():
    id_token = request.json.get('idToken')
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        user_email = decoded_token.get('email', '')

        # Store session
        session['user'] = {'uid': user_id, 'email': user_email}

        # Store session in Firebase DB
        db.reference(f'sessions/{user_id}').set({'email': user_email})

        return jsonify({'success': True, 'message': 'Authentication successful'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 401

@app.route('/logout')
def logout():
    if 'user' in session:
        user_id = session['user']['uid']
        db.reference(f'sessions/{user_id}').delete()  # Remove session from Firebase DB
        session.pop('user')  # Remove from Flask session

    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
