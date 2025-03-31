import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import os
import random

from dotenv import load_dotenv
load_dotenv()
sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("EMAIL_PASSWORD")

def validate_email(email):
    """Validate email format using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def send_email(sender_email, password, receiver_email, html_template):
    """Send an email with HTML content."""
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Webtech Password Manager - Email Verification Code"
    msg.attach(MIMEText(html_template, "html"))
    try:
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login(sender_email, password)
        smtp_server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email successfully sent!")
    except smtplib.SMTPAuthenticationError:
        print("Authentication Error: Please check your email credentials.")
    except smtplib.SMTPConnectError:
        print("Connection Error: Unable to connect to the SMTP server.")
    except Exception as e:
        print(f"Error: unable to send email - {str(e)}")
    finally:
        smtp_server.quit()

def otp_generator():
    """Generate a random OTP."""
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    length = 6
    OTP = "".join(random.sample(characters, length))
    return OTP

if __name__ == "__main__":
    # Securely fetch sender email and password from environment variables
    sender_email = os.getenv("SENDER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not password:
        print("Error: Please set the environment variables 'SENDER_EMAIL' and 'EMAIL_PASSWORD'.")
        exit()

    receiver_email = input("Enter receiver email: ").strip()

    if not validate_email(receiver_email):
        print("Invalid email format. Please try again.")
    else:
        # Generate OTP and update the HTML template dynamically
        otp = otp_generator()
        username = receiver_email.split("@")[0]  # Extract username from email
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Verification</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f7; text-align: center; padding: 20px;">
    <div style="max-width: 480px; background: #ffffff; padding: 30px; border-radius: 8px; 
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); margin: auto;">
        <h1 style="color: #333; font-size: 22px;">Email Verification</h1>
        <p style="color: #555; font-size: 16px; line-height: 1.6;">
            Hello <strong>{username}</strong>,
        </p>
        <p style="color: #555; font-size: 16px;">
            Use the code below to verify your email address:
        </p>

        <!-- OTP Boxes with More Space -->
        <div style="display: flex; justify-content: center; align-items: center; gap: 15px; margin: 20px 0;">
            <div style="width: 50px; height: 50px; background: #007bff; color: #ffffff; 
                        font-size: 24px; font-weight: bold; text-align: center; 
                        display: flex; justify-content: center; align-items: center; 
                        border-radius: 8px;">{otp[0]}</div>
            <div style="width: 50px; height: 50px; background: #007bff; color: #ffffff; 
                        font-size: 24px; font-weight: bold; text-align: center; 
                        display: flex; justify-content: center; align-items: center; 
                        border-radius: 8px;">{otp[1]}</div>
            <div style="width: 50px; height: 50px; background: #007bff; color: #ffffff; 
                        font-size: 24px; font-weight: bold; text-align: center; 
                        display: flex; justify-content: center; align-items: center; 
                        border-radius: 8px;">{otp[2]}</div>

            <div style="font-size: 28px; font-weight: bold; color: #333;">-</div>

            <div style="width: 50px; height: 50px; background: #007bff; color: #ffffff; 
                        font-size: 24px; font-weight: bold; text-align: center; 
                        display: flex; justify-content: center; align-items: center; 
                        border-radius: 8px;">{otp[3]}</div>
            <div style="width: 50px; height: 50px; background: #007bff; color: #ffffff; 
                        font-size: 24px; font-weight: bold; text-align: center; 
                        display: flex; justify-content: center; align-items: center; 
                        border-radius: 8px;">{otp[4]}</div>
            <div style="width: 50px; height: 50px; background: #007bff; color: #ffffff; 
                        font-size: 24px; font-weight: bold; text-align: center; 
                        display: flex; justify-content: center; align-items: center; 
                        border-radius: 8px;">{otp[5]}</div>
        </div>

        <p style="font-size: 12px; color: #888; margin-top: 20px;">
            If you did not request this, please ignore this email or contact support.
        </p>
    </div>
</body>
</html>
"""


        send_email(sender_email, password, receiver_email, html_template)