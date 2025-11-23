# email_sender.py

# PART 1: Import necessary libraries
import smtplib  # For sending emails
from email.mime.multipart import MIMEMultipart  # For creating email structure
from email.mime.text import MIMEText  # For email body text
from email.mime.base import MIMEBase  # For attaching files
from email import encoders  # For encoding attachments
import pandas as pd  # For reading CSV file
import time  # For delays between emails
from datetime import datetime  # For timestamps

# PART 2: Define the Email Bot Class
class ResumeEmailBot:
    def __init__(self, sender_email, sender_password, smtp_server="smtp.gmail.com", smtp_port=587):
        """
        Initialize the bot with your email credentials
        
        What this does:
        - Stores your email and password
        - Sets up Gmail's SMTP server (you can change for other providers)
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        
    def create_message(self, recruiter_name, recruiter_email, company_name, position, resume_path):
        """
        Creates a personalized email message
        
        What this does:
        - Creates email with To, From, Subject
        - Writes personalized body text
        - Attaches your resume PDF
        """
        # Create email container
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recruiter_email
        msg['Subject'] = f"Application for {position} Position"
        
        # Personalized email body
        # CUSTOMIZE THIS PART WITH YOUR DETAILS!
        body = f"""Dear {recruiter_name},

I hope this email finds you well. I am writing to express my strong interest in the {position} position at {company_name}.

With my background and skills, I believe I would be a valuable addition to your team. I have attached my resume for your review, which provides detailed information about my experience and qualifications.

I would welcome the opportunity to discuss how my skills and experience align with your needs. Thank you for considering my application.

Best regards,
[Your Full Name]
[Your Phone Number]
[Your Email]
[Your LinkedIn Profile URL]"""
        
        # Attach the body text
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach resume file
        try:
            with open(resume_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                filename = resume_path.split("/")[-1]  # Get just the filename
                part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                msg.attach(part)
        except Exception as e:
            print(f"❌ Error attaching resume: {e}")
            
        return msg
    
    def send_email(self, msg, recruiter_email):
        """
        Sends a single email
        
        What this does:
        - Connects to email server
        - Logs in with your credentials
        - Sends the email
        - Closes connection
        """
        try:
            # Connect to Gmail's server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Secure the connection
            
            # Login
            server.login(self.sender_email, self.sender_password)
            
            # Send email
            server.send_message(msg)
            
            # Close connection
            server.quit()
            return True
        except Exception as e:
            print(f"❌ Failed to send email to {recruiter_email}: {e}")
            return False
    
    def send_bulk_emails(self, csv_file, resume_path, delay=5):
        """
        Sends emails to all recruiters in CSV file
        
        What this does:
        - Reads CSV file
        - Loops through each recruiter
        - Sends personalized email to each
        - Waits between emails to avoid spam filters
        """
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        total = len(df)
        sent = 0
        failed = 0
        
        print(f"\n{'='*60}")
        print(f"📧 Starting to send {total} emails...")
        print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Loop through each recruiter
        for idx, row in df.iterrows():
            recruiter_name = row['name']
            recruiter_email = row['email']
            company_name = row['company']
            position = row['position']
            
            print(f"📤 [{idx+1}/{total}] Sending to {recruiter_name} at {company_name}...")
            
            # Create personalized message
            msg = self.create_message(recruiter_name, recruiter_email, company_name, position, resume_path)
            
            # Send the email
            if self.send_email(msg, recruiter_email):
                sent += 1
                print(f"✅ Successfully sent to {recruiter_email}")
            else:
                failed += 1
                print(f"❌ Failed to send to {recruiter_email}")
            
            print()  # Blank line for readability
            
            # Wait before sending next email (prevents spam detection)
            if idx < total - 1:  # Don't wait after last email
                print(f"⏳ Waiting {delay} seconds before next email...\n")
                time.sleep(delay)
        
        # Print summary
        print(f"{'='*60}")
        print(f"📊 EMAIL SENDING COMPLETED!")
        print(f"{'='*60}")
        print(f"✅ Total Sent: {sent}")
        print(f"❌ Failed: {failed}")
        print(f"📝 Total: {total}")
        print(f"🕐 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")


# PART 3: Main execution code
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 AUTOMATED RESUME EMAIL SENDER BOT")
    print("="*60 + "\n")
    
    # ============================================
    # CONFIGURATION - CHANGE THESE VALUES!
    # ============================================
    
    YOUR_EMAIL = "akashctk123@gmail.com"  # ← Change this!
    YOUR_APP_PASSWORD = "obbz uoqp wlry fomc"  # ← Change this! (16-char app password)
    RESUME_PATH = "AKASH_N_RESUME.pdf"  # ← Change if your resume has different name
    CSV_FILE = "recruiters.csv"  # ← Change if your CSV has different name
    
    # ============================================
    
    # Create the bot
    print("🔧 Initializing email bot...")
    bot = ResumeEmailBot(YOUR_EMAIL, YOUR_APP_PASSWORD)
    
    # Send emails to all recruiters
    print("✅ Bot initialized successfully!\n")
    bot.send_bulk_emails(CSV_FILE, RESUME_PATH, delay=5)
    
    print("🎉 All done! Check your sent folder to verify.")