from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy  # Use SQLAlchemy for database
from routes.predict import predict_blueprint
from routes.auth import auth
from routes.api import api
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT
import hashlib
import random
import mysql.connector

# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = 'supersecretkey'  # Required for session and flash

# MySQL Configuration
app.config["MYSQL_DATABASE_HOST"] = MYSQL_HOST
app.config["MYSQL_DATABASE_USER"] = MYSQL_USER
app.config["MYSQL_DATABASE_PASSWORD"] = MYSQL_PASSWORD
app.config["MYSQL_DATABASE_DB"] = MYSQL_DB
app.config["MYSQL_DATABASE_PORT"] = MYSQL_PORT
app.config["MYSQL_DB"] = MYSQL_DB

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'         # 🔁 Change this
app.config['MAIL_PASSWORD'] = 'your_app_password_here'       # 🔁 Change this
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'   # 🔁 Change this

mail = Mail(app)

# Function to get a database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=MYSQL_PORT
    )
    return conn

# Register Blueprints
app.register_blueprint(predict_blueprint, url_prefix="/predict")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(api, url_prefix="/api")

# Root redirects to login page
@app.route('/')
def root():
    return redirect(url_for('login'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_username = request.form['username']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s OR username = %s",
                           (email_or_username, email_or_username))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user and user['password_hash'] == password:
                return redirect(url_for('home'))
            else:
                return render_template('login.html', message="❌ Invalid username or password")
        except Exception as e:
            return render_template('login.html', message=f"❌ Error during login: {e}")

    return render_template('login.html')

# Home Page after login
@app.route('/home')
def home():
    return render_template('index.html')

# Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, password))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('login', message='Signup successful! Please log in.'))
        except Exception as e:
            return f"❌ Error during signup: {e}"
    return render_template('signup.html')

# Forgot Password Page with OTP Sending
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        session["otp"] = otp
        session["reset_email"] = email

        try:
            msg = Message("Your OTP Code", recipients=[email])
            msg.body = f"Your OTP for password reset is: {otp}"
            mail.send(msg)
            flash("✅ OTP sent to your email.")
            return redirect(url_for("verify_otp"))
        except Exception as e:
            flash(f"❌ Failed to send OTP: {e}")
            return redirect(url_for("forgot_password"))

    return render_template("forgot-password.html")

# Verify OTP Route
@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    if request.method == "POST":
        entered_otp = request.form["otp"]
        if entered_otp == session.get("otp"):
            flash("✅ OTP Verified! You may now reset your password.")
            return redirect(url_for("reset_password"))
        else:
            flash("❌ Invalid OTP. Try again.")
    return render_template("verify-otp.html")

# Reset Password Page
@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        new_password = request.form["password"]
        email = session.get("reset_email")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password_hash = %s WHERE email = %s", (new_password, email))
            conn.commit()
            cursor.close()
            conn.close()
            flash("✅ Password reset successfully! You can now log in.")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"❌ Failed to reset password: {e}")
            return redirect(url_for("reset_password"))

    return render_template("reset-password.html")

# Prediction route
@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

# Result route
@app.route('/result')
def result():
    return render_template('result.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
