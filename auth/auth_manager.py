import sys
import os
import bcrypt
import re
from datetime import datetime, timezone, timedelta
from tabulate import tabulate
import msvcrt  # For Windows keyboard input
import time
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Adjust sys.path to include parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import database connection
from db.db_connect import db_name

# Load environment variables
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

class AuthManager:
    def __init__(self):
        self.current_user = None
        self.user_collection = db_name['users']
        self.otp_collection = db_name['otps']  # New collection for OTPs

    def handle_special_key(self, key):
        """Handle special keys"""
        if key == b'\x1b':  # ESC
            return 'ESC'
        elif key == b'\x08':  # Backspace
            return 'BACKSPACE'
        elif key == b'\x7f':  # Delete
            return 'DELETE'
        elif key == b'\x03':  # Ctrl+C
            return 'CTRL+C'
        return None

    def get_input(self, prompt):
        """Get input with special key support"""
        print(prompt, end='', flush=True)
        value = ""
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                special_key = self.handle_special_key(key)
                
                if special_key == 'ESC':
                    print("\nOperation cancelled.")
                    return None
                elif special_key == 'BACKSPACE':
                    if value:
                        value = value[:-1]
                        print('\b \b', end='', flush=True)
                    continue
                elif special_key == 'CTRL+C':
                    raise KeyboardInterrupt
                elif key == b'\r':  # Enter key
                    break
                else:
                    # Handle regular character input
                    try:
                        char = key.decode()
                        value += char
                        print(char, end='', flush=True)
                        continue
                    except UnicodeDecodeError:
                        continue
            time.sleep(0.1)  # Small delay to prevent CPU overuse
        return value.strip()

    def generate_otp(self):
        """Generate a random OTP"""
        characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        length = 6
        return "".join(random.sample(characters, length))

    def send_verification_email(self, email, otp, username):
        """Send verification email with OTP"""
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = email
        msg["Subject"] = "Password Manager - Email Verification Code"
        
        expiration_time = datetime.now() + timedelta(minutes=10)
        expiration_time_str = expiration_time.strftime("%I:%M %p")

        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Verification</title>
    <style>
        .otp-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: nowrap;
        }}
        .otp-box {{
            width: 40px;
            height: 40px;
            background: #28a745;
            color: #ffffff;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 0 2px;
        }}
        .button-container {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 20px 0;
        }}
        .button {{
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }}
        .copy-button {{
            background-color: #28a745;
        }}
        .copy-button:hover {{
            background-color: #218838;
            transform: translateY(-2px);
        }}
        .expiry {{
            font-size: 14px;
            color: #d9534f;
            font-weight: bold;
            margin: 15px 0;
            padding: 10px;
            background: #fff3f3;
            border-radius: 5px;
        }}
        .warning {{
            font-size: 12px;
            color: #888;
            margin-top: 20px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
        }}
    </style>
    <script>
        function copyToClipboard(text) {{
            const textarea = document.createElement('textarea');
            textarea.value = text;
            document.body.appendChild(textarea);
            textarea.select();
            try {{
                document.execCommand('copy');
                alert('Code copied to clipboard!');
            }} catch (err) {{
                console.error('Failed to copy text: ', err);
            }}
            document.body.removeChild(textarea);
        }}
    </script>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f7; text-align: center; padding: 20px;">
    <div style="max-width: 480px; background: #ffffff; padding: 30px; border-radius: 8px; 
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); margin: auto;">
        <h1 style="color: #333; font-size: 22px; margin-bottom: 20px;">Email Verification</h1>
        <p style="color: #555; font-size: 16px; line-height: 1.6;">
            Hello <strong>{username}</strong>,
        </p>
        <p style="color: #555; font-size: 16px;">
            Use the code below to verify your email address:
        </p>

        <div class="otp-container">
            <div class="otp-box">{otp[0]}</div>
            <div class="otp-box">{otp[1]}</div>
            <div class="otp-box">{otp[2]}</div>
            <div class="otp-box">{otp[3]}</div>
            <div class="otp-box">{otp[4]}</div>
            <div class="otp-box">{otp[5]}</div>
        </div>

        <div class="button-container">
            <a href="#" class="button copy-button" onclick="copyToClipboard('{otp}'); return false;">
                Copy Code
            </a>
        </div>

        <div class="expiry">
            OTP Expires at: <strong>{expiration_time_str}</strong>
        </div>

        <div class="warning">
            If you did not request this, please ignore this email or contact support.
        </div>
    </div>
</body>
</html>
"""
        msg.attach(MIMEText(html_template, "html"))
        
        try:
            smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
            smtp_server.starttls()
            smtp_server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, email, msg.as_string())
            print("\nVerification email sent successfully!")
            return True
        except Exception as e:
            print(f"\nError sending verification email: {str(e)}")
            return False
        finally:
            smtp_server.quit()

    def verify_otp(self, email, otp):
        """Verify the OTP for email verification"""
        otp_record = self.otp_collection.find_one({
            "email": email.lower(),
            "otp": otp,
            "expires_at": {"$gt": datetime.now()}
        })
        
        if otp_record:
            self.otp_collection.delete_one({"_id": otp_record["_id"]})
            return True
        return False

    def hash_password(self, password):
        """Hashes the password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify_password(self, password, hashed_password):
        """Verifies the password against its hash"""
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def is_valid_email(self, email):
        """Validates email format"""
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email)

    def register(self):
        try:
            print("\n=== User Registration ===")
            
            # Keep asking for username until a unique one is provided or user cancels
            while True:
                username = self.get_input("\nEnter username (Press ESC to cancel): ")
                if not username:  # User pressed ESC
                    return False
                
                # Check if username already exists
                if self.user_collection.find_one({"username": username.lower()}):
                    print("\nUsername already exists. Please choose another.")
                    continue
                break  # Username is unique, proceed with registration

            email = self.get_input("\nEnter email (Press ESC to cancel): ")
            if not email:
                return False

            if not self.is_valid_email(email):
                print("\nInvalid email format.")
                return False

            # Check if email already exists
            if self.user_collection.find_one({"email": email.lower()}):
                print("\nEmail is already registered.")
                return False

            password = self.get_input("\nEnter password (Press ESC to cancel): ")
            if not password:
                return False

            confirm_password = self.get_input("\nConfirm password (Press ESC to cancel): ")
            if not confirm_password:
                return False

            if password != confirm_password:
                print("\nPasswords do not match.")
                return False

            # Generate and send OTP
            otp = self.generate_otp()
            expiration_time = datetime.now() + timedelta(minutes=10)
            
            # Store OTP in database
            self.otp_collection.insert_one({
                "email": email.lower(),
                "otp": otp,
                "expires_at": expiration_time
            })

            # Send verification email
            if not self.send_verification_email(email, otp, username):
                print("\nFailed to send verification email. Please try again.")
                return False

            print("\nPlease check your email for the verification code.")
            print("The code will expire in 10 minutes.")

            # Verify OTP
            max_attempts = 3
            attempts = 0
            verified = False
            
            while attempts < max_attempts and not verified:
                verification_otp = self.get_input("\nEnter verification code (Press ESC to cancel): ")
                if not verification_otp:  # User pressed ESC
                    print("\nRegistration cancelled.")
                    return False

                if self.verify_otp(email, verification_otp):
                    print("\nEmail verified successfully!")
                    verified = True
                else:
                    attempts += 1
                    if attempts < max_attempts:
                        print(f"\nInvalid or expired verification code. {max_attempts - attempts} attempts remaining.")
                        print("Please check your email and try again.")
                    else:
                        print("\nMaximum verification attempts reached. Registration cancelled.")
                        return False

            if not verified:
                print("\nEmail verification failed. Registration cancelled.")
                return False

            # Hash the password before storing
            hashed_password = self.hash_password(password)
            
            # Create new user document
            user_data = {
                "username": username.lower(),
                "email": email.lower(),
                "password_hash": hashed_password,
                "created_at": datetime.now(timezone.utc),
                "data": [],  # Initialize empty data array
                "email_verified": True
            }

            self.user_collection.insert_one(user_data)
            print("\nRegistration successful!")
            return True
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return False
        except Exception as e:
            print(f"\nRegistration failed: {e}")
            return False

    def login(self):
        try:
            print("\n=== User Login ===")
            username = self.get_input("\nEnter username (Press ESC to cancel): ")
            if not username:
                return False

            password = self.get_input("\nEnter password (Press ESC to cancel): ")
            if not password:
                return False

            # Find user by username
            user = self.user_collection.find_one({"username": username.lower()})
            
            if user and self.verify_password(password, user.get("password_hash", "")):
                if not user.get("email_verified", False):
                    print("\nPlease verify your email before logging in.")
                    return False
                    
                self.current_user = {
                    "username": username.lower(),
                    "email": user.get("email"),
                    "user_id": str(user.get("_id"))
                }
                print("\nLogin successful!")
                return True
            else:
                print("\nInvalid username or password.")
                return False
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return False
        except Exception as e:
            print(f"\nLogin failed: {e}")
            return False

    def logout(self):
        if self.current_user:
            print(f"\nLogging out user: {self.current_user['username']}")
            self.current_user = None
        else:
            print("\nNo user is currently logged in.")

    def is_logged_in(self):
        return self.current_user is not None

    def get_current_user(self):
        return self.current_user

    def show_menu(self):
        while True:
            try:
                print("\n=== Authentication Menu ===")
                print("1. Register")
                print("2. Login")
                print("3. Exit")
                print("\nPress ESC at any time to return to menu")
                print("Press Ctrl+C to exit")

                choice = self.get_input("\nEnter your choice: ")
                if not choice:  # ESC was pressed
                    continue

                if choice == "1":
                    self.register()
                elif choice == "2":
                    if self.login():
                        return True
                elif choice == "3":
                    print("\nExiting Authentication Menu. Goodbye!")
                    return False
                else:
                    print("\nInvalid choice. Please select a valid option.")
            except KeyboardInterrupt:
                print("\n\nExiting Password Manager. Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("Returning to menu...")

    def forgot_password(self):
        """Handle forgot password request"""
        try:
            print("\n=== Forgot Password ===")
            email = self.get_input("\nEnter your registered email (Press ESC to cancel): ")
            if not email:
                return False

            if not self.is_valid_email(email):
                print("\nInvalid email format.")
                return False

            # Check if email exists
            user = self.user_collection.find_one({"email": email.lower()})
            if not user:
                print("\nEmail not found. Please check your email or register if you haven't already.")
                return False

            # Generate reset code
            reset_code = self.generate_otp()
            expiration_time = datetime.now() + timedelta(minutes=10)
            
            # Store reset code in database
            self.otp_collection.insert_one({
                "email": email.lower(),
                "otp": reset_code,
                "expires_at": expiration_time,
                "type": "password_reset"
            })

            # Send reset email
            if not self.send_reset_email(email, reset_code, user["username"]):
                print("\nFailed to send reset email. Please try again.")
                return False

            print("\nPlease check your email for the reset code.")
            print("The code will expire in 10 minutes.")

            # Verify reset code
            max_attempts = 3
            attempts = 0
            verified = False
            
            while attempts < max_attempts and not verified:
                print("\nOptions:")
                print("1. Enter reset code")
                print("2. Resend code")
                print("3. Cancel")
                print("\nPress ESC at any time to cancel")
                
                choice = self.get_input("\nEnter your choice: ")
                if not choice:  # User pressed ESC
                    print("\nPassword reset cancelled.")
                    return False

                if choice == "1":
                    verification_code = self.get_input("\nEnter reset code: ")
                    if not verification_code:  # User pressed ESC
                        continue

                    if self.verify_otp(email, verification_code):
                        print("\nReset code verified successfully!")
                        verified = True
                    else:
                        attempts += 1
                        if attempts < max_attempts:
                            print(f"\nInvalid or expired reset code. {max_attempts - attempts} attempts remaining.")
                            print("Please check your email and try again.")
                        else:
                            print("\nMaximum verification attempts reached. Password reset cancelled.")
                            return False
                elif choice == "2":
                    # Generate new reset code
                    reset_code = self.generate_otp()
                    expiration_time = datetime.now() + timedelta(minutes=10)
                    
                    # Update reset code in database
                    self.otp_collection.update_one(
                        {"email": email.lower(), "type": "password_reset"},
                        {"$set": {
                            "otp": reset_code,
                            "expires_at": expiration_time
                        }}
                    )

                    # Send new reset email
                    if self.send_reset_email(email, reset_code, user["username"]):
                        print("\nNew reset code sent successfully!")
                        print("The code will expire in 10 minutes.")
                    else:
                        print("\nFailed to send new reset code. Please try again.")
                elif choice == "3":
                    print("\nPassword reset cancelled.")
                    return False
                else:
                    print("\nInvalid choice. Please select a valid option.")

            if not verified:
                print("\nReset code verification failed. Please try again.")
                return False

            # Get new password
            new_password = self.get_input("\nEnter new password (Press ESC to cancel): ")
            if not new_password:
                return False

            confirm_password = self.get_input("\nConfirm new password (Press ESC to cancel): ")
            if not confirm_password:
                return False

            if new_password != confirm_password:
                print("\nPasswords do not match.")
                return False

            # Update password
            hashed_password = self.hash_password(new_password)
            self.user_collection.update_one(
                {"email": email.lower()},
                {"$set": {"password_hash": hashed_password}}
            )

            print("\nPassword reset successful!")
            return True

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return False
        except Exception as e:
            print(f"\nPassword reset failed: {e}")
            return False

    def send_reset_email(self, email, reset_code, username):
        """Send password reset email"""
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = email
        msg["Subject"] = "Password Manager - Reset Your Password"
        
        expiration_time = datetime.now() + timedelta(minutes=10)
        expiration_time_str = expiration_time.strftime("%I:%M %p")

        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reset Your Password</title>
    <style>
        .reset-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: nowrap;
        }}
        .reset-box {{
            width: 40px;
            height: 40px;
            background: #28a745;
            color: #ffffff;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 0 2px;
        }}
        .button-container {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 20px 0;
        }}
        .button {{
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }}
        .copy-button {{
            background-color: #28a745;
        }}
        .copy-button:hover {{
            background-color: #218838;
            transform: translateY(-2px);
        }}
        .expiry {{
            font-size: 14px;
            color: #d9534f;
            font-weight: bold;
            margin: 15px 0;
            padding: 10px;
            background: #fff3f3;
            border-radius: 5px;
        }}
        .warning {{
            font-size: 12px;
            color: #888;
            margin-top: 20px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
        }}
    </style>
    <script>
        function copyToClipboard(text) {{
            const textarea = document.createElement('textarea');
            textarea.value = text;
            document.body.appendChild(textarea);
            textarea.select();
            try {{
                document.execCommand('copy');
                alert('Code copied to clipboard!');
            }} catch (err) {{
                console.error('Failed to copy text: ', err);
            }}
            document.body.removeChild(textarea);
        }}
    </script>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f7; text-align: center; padding: 20px;">
    <div style="max-width: 480px; background: #ffffff; padding: 30px; border-radius: 8px; 
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); margin: auto;">
        <h1 style="color: #333; font-size: 22px; margin-bottom: 20px;">Reset Your Password</h1>
        <p style="color: #555; font-size: 16px; line-height: 1.6;">
            Hello <strong>{username}</strong>,
        </p>
        <p style="color: #555; font-size: 16px;">
            Use the code below to reset your password:
        </p>

        <div class="reset-container">
            <div class="reset-box">{reset_code[0]}</div>
            <div class="reset-box">{reset_code[1]}</div>
            <div class="reset-box">{reset_code[2]}</div>
            <div class="reset-box">{reset_code[3]}</div>
            <div class="reset-box">{reset_code[4]}</div>
            <div class="reset-box">{reset_code[5]}</div>
        </div>

        <div class="button-container">
            <a href="#" class="button copy-button" onclick="copyToClipboard('{reset_code}'); return false;">
                Copy Code
            </a>
        </div>

        <div class="expiry">
            Reset Code Expires at: <strong>{expiration_time_str}</strong>
        </div>

        <div class="warning">
            If you did not request this, please ignore this email or contact support.
        </div>
    </div>
</body>
</html>
"""
        msg.attach(MIMEText(html_template, "html"))
        
        try:
            smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
            smtp_server.starttls()
            smtp_server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, email, msg.as_string())
            print("\nReset email sent successfully!")
            return True
        except Exception as e:
            print(f"\nError sending reset email: {str(e)}")
            return False
        finally:
            smtp_server.quit() 