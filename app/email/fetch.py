import os
import imaplib
from dotenv import load_dotenv

load_dotenv()

def fetch_emails():

    email=os.getenv('GMAIL_MAIL')
    pwd=os.getenv('GMAIL_PASSWORD')

    mail = imaplib.IMAP4_SSL('imap.gmail.com')

    mail.login(email,pwd)

    mail.select('inbox')

    status, message_ids = mail.search(None, 'FROM "noreply@statuspage.io"')

    email_ids = message_ids[0].split()


    for eid in email_ids:
        # Fetch and process email
       print(eid)
    
    mail.logout()

    return email_ids