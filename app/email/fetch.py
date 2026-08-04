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

email_ids=[b'31099',
b'31100',
b'31101',
b'31118',
b'31119',
b'31120']

print(email_ids)

import imaplib
import email
from email.policy import default

# Configuration
imap_server = "imap.gmail.com"
username = os.getenv('GMAIL_MAIL')
password = os.getenv('GMAIL_PASSWORD')
target_message_id = "noreply@statuspage.io" # The specific Message-ID header value

# Connect
mail = imaplib.IMAP4_SSL(imap_server)
mail.login(username, password)
mail.select("inbox")

e_id=b'31099'
try:
        # Fetch by ID
        status, msg_data = mail.fetch(e_id, '(RFC822)')
        print("MSG_DATA")
        
        if status == 'OK' and msg_data[0][1]:
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email , policy=default)
            print(dir(msg))
            print(f"ID: {e_id.decode()} | Subject: {msg['Subject']}")
            print(msg.is_multipart())

            for i in msg.walk():
                if i.get_content_type() == "text/plain":
                    body = i.get_content()
                    print(body)
            
        else:
            print(f"ID: {e_id.decode()} | Not found or error.")
            
except Exception as e:
        print(f"Error fetching ID: {e}")

mail.close()
mail.logout()   