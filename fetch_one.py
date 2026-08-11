import os
import imaplib
from dotenv import load_dotenv

import email
from email.policy import default

import re

load_dotenv()
email_cred=os.getenv('GMAIL_MAIL')
pwd_cred=os.getenv('GMAIL_PASSWORD')
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email_cred,pwd_cred)
mail.select('inbox')

status, message_ids = mail.search(None, 'FROM "noreply@statuspage.io"')


def fetch_body(mail,eid):
    print("INside fetch_body with : ",eid)
    try:
            # Fetch by ID
            status, msg_data = mail.fetch(eid, '(RFC822)')
            if status == 'OK' and msg_data[0][1]:
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email , policy=default)
                for i in msg.walk():
                    if i.get_content_type() == "text/plain":
                        body = i.get_content() 
                
                return  body       
               
            else:
                return False
    except Exception as e:
        print("Exception",e)
        return False
body=fetch_body(mail,b'24650')
print(body)

pattern=r"Time posted\s+([A-Z][a-z]{2}\s+\d{1,2},\s+\d{2}:\d{2}\s+UTC)"
match=re.search(pattern,body)
if match:
    timestamp = match.group(1)
    print(timestamp) 