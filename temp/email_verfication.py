import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import os
import random

def validate_email(email):
    """Validate email format using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def send_email(sender_email, password, receiver_email,  html_template):
    """Send an email with HTML content."""
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Webtech Password Manager - [Email Verification code]"
    msg.attach(MIMEText(html_template, "html"))
    try:
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login(sender_email, password)
        smtp_server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email successfully sent!")
    except Exception as e:
        print("Error: unable to send email", str(e))
    finally:
        smtp_server.quit()

def verify_email(receiver_email):
    """Verify the receiver email."""
    try:
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        result = smtp_server.verify(receiver_email)
        print(f"Verification result: {result}")
    except Exception as e:
        print(f"Verification failed: {e}")
    finally:
        smtp_server.quit()


def otp_genarater():
    """Generate a random  OTP."""
    numbers= "0123456789"
    small_letters="abcdefghijklmnopqrstuvwxyz"
    capital_letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    all_characters=numbers+small_letters+capital_letters
    length=6
    OTP="".join(random.sample(all_characters,length))
    return OTP
    

if __name__ == "__main__":
    sender_email = os.getenv("SENDER_EMAIL")  # Use environment variables for security
    password = os.getenv("EMAIL_PASSWORD")
    receiver_email = input("Enter receiver email: ").strip()

    if not validate_email(receiver_email):
        print("Invalid email format. Please try again.")
    else:
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Verification</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f9;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    text-align: center;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    color: #333333;
                }
                p {
                    color: #555555;
                    margin: 10px 0;
                }
                .button {
                    display: inline-block;
                    padding: 10px 20px;
                    color: #ffffff;
                    background-color: #4caf50;
                    text-decoration: none;
                    border-radius: 5px;
                    font-size: 16px;
                    margin-top: 10px;
                }
                .button:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Email Verification</h1>
                <p>Hi [User],</p>
                <p>Thank you for signing up! Please verify your email by clicking the button below.</p>
                <!-- <a href="[Verification Link]" class="button">Verify Email</a> -->
                <p>Your verification code is: [OTP]</p>
                <p>If you didn't request this, please ignore this email.</p>
            </div>
        </body>
        </html>
        """
        verify_email(receiver_email)
        sender_email="t99527506@gmail.com"
        password="glzw ketb vhno cyov"
        send_email(sender_email, password, receiver_email,  html_template)


