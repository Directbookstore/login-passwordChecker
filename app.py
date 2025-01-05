from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import string

app = Flask(__name__)

# List of common passwords
common_passwords = [
    "123456", "password", "123456789", "12345678", "12345", "1234567",
    "qwerty", "abc123", "password1", "123123", "admin", "letmein", "welcome"
]

# Function to check password strength
def check_password_strength(password):
    feedback = []
    is_strong = True
    score = 0

    # Length criteria
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")
        is_strong = False

    # Uppercase criteria
    if any(char.isupper() for char in password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")
        is_strong = False

    # Lowercase criteria
    if any(char.islower() for char in password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")
        is_strong = False

    # Numbers criteria
    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("Include numbers.")
        is_strong = False

    # Special characters criteria
    if any(char in "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~" for char in password):
        score += 1
    else:
        feedback.append("Add special characters.")
        is_strong = False

    # Common passwords check
    if password in common_passwords:
        feedback.append("Avoid using common passwords.")
        is_strong = False

    # Strength level
    if score <= 2:
        strength = "Weak"
    elif score == 3:
        strength = "Moderate"
    else:
        strength = "Strong"

    return strength, feedback

# Function to generate a random password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~"
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    # Simple validation (you can add more robust checks)
    if username == "admin" and password == "admin123":
        return redirect(url_for('index'))
    else:
        return render_template('login.html', error="Invalid username or password")

@app.route('/password_checker')
def index():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    password = request.form['password']
    strength, feedback = check_password_strength(password)
    suggested_password = generate_password() if strength != "Strong" else None
    return jsonify({"strength": strength, "feedback": feedback, "suggested_password": suggested_password})

if __name__ == '__main__':
    app.run(debug=True)
