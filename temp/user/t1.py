import sys
import os
import bcrypt
import re
import random
from datetime import datetime, timezone
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Connect to MongoDB
from db.db_connect import db_name
user_collection = db_name['users']

def hash_password(password):
    """Hashes the password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def is_valid_email(email):
    """Validates email format"""
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email)

def generate_otp():
    """Generate a 6-digit numeric OTP"""
    return str(random.randint(100000, 999999))

def send_email_otp(receiver_email, otp):
    """Sends an OTP to the user's email for verification"""
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = "Your OTP for Password Manager Registration"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px;">
        <h2>Email Verification</h2>
        <p>Your One-Time Password (OTP) for verification is:</p>
        <h1 style="color: red;">{otp}</h1>
        <p>Please enter this code to complete your registration.</p>
        <p><b>Note:</b> This OTP is valid for 10 minutes.</p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html"))

    try:
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        smtp_server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        smtp_server.quit()
        print("\n✅ OTP sent to your email. Please check your inbox.")
        return True
    except smtplib.SMTPAuthenticationError:
        print("\n❌ Authentication Error: Please check your email credentials.")
    except Exception as e:
        print(f"\n❌ Error sending email: {e}")
    return False

print("Create an account:")
while True:
    username = input("Username: ").strip().lower()

    if not username:
        print("\nUsername cannot be empty.\n")
        continue

    # Check if username already exists
    if user_collection.find_one({"username": username}):
        print("\n❌ Username already exists. Try another.\n")
        continue

    email = input("Email: ").strip().lower()

    if not email:
        print("\nEmail cannot be empty.\n")
        continue

    if not is_valid_email(email):
        print("\n❌ Invalid email format.\n")
        continue

    # Check if email already exists
    if user_collection.find_one({"email": email}):
        print("\n❌ Email is already registered.\n")
        continue

    otp = generate_otp()

    # Send OTP to email
    if not send_email_otp(email, otp):
        print("\n❌ Email verification failed. Please try again.")
        continue

    # Ask user to enter OTP
    user_otp = input("\nEnter OTP sent to your email: ").strip()

    if user_otp != otp:
        print("\n❌ Incorrect OTP. Registration failed. Please try again.\n")
        continue

    password = input("Password: ").strip()

    if not password:
        print("\n❌ Password cannot be empty.\n")
        continue

    hashed_password = hash_password(password)

    # Insert new user into the database
    user_data = {
        "username": username,
        "email": email,
        "password_hash": hashed_password,
        "created_at": datetime.now(timezone.utc)  # Fixed deprecated UTC warning
    }

    user_collection.insert_one(user_data)

    print("\n✅ Account created successfully!\n")
    break  # Exit loop after successful registration
