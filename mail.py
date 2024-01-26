import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, message, sender_email, receiver_email, password):
    # Set up the MIME
    email = MIMEMultipart()
    email["From"] = sender_email
    email["To"] = receiver_email
    email["Subject"] = subject

    # Add body to email
    email.attach(MIMEText(message, "html"))

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        # Establish a secure SMTP connection with the server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, email.as_string())
        print(f"[+] Email sent successfully to {receiver_email}...")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

# Usage example
sender_email = ""  #Sender email address
receiver_email = ""  #Recipient's email address
password = ""  #Sender email account password
subject = "" #mail Subject
message = "" #mail body 

if __name__ == '__main__':
  send_email(subject, message, sender_email, receiver_email, password)
