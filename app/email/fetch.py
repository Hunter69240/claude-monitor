import os
import imaplib
from dotenv import load_dotenv

import email
from email.policy import default
load_dotenv()
import re



KNOWN_MODELS = [
        "Mythos 5" ,
        "Fable 5"  ,
        "Opus 5"   ,
        "Sonnet 5"  ,
        "Haiku 4.5",
        "Opus 4.8" , 
        "Opus 4.7",
        "Opus 4.6" , 
        "Opus 3" , 
        "Sonnet 4.6"        
]


def fetch_emails():

    email_cred=os.getenv('GMAIL_MAIL')
    pwd_cred=os.getenv('GMAIL_PASSWORD')

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_cred,pwd_cred)
    mail.select('inbox')

    status, message_ids = mail.search(None, 'FROM "noreply@statuspage.io"')

    email_ids = message_ids[0].split()

    count=0
    records=[]
    for eid in email_ids:
        if count ==20:
            break
        record={}
        record["email_id"]=eid
        record["body"] = fetch_body(mail,eid)
        if record["body"] == False:
            continue # Later think of logging
        record["model"] = fetch_model(record["body"])
        record["timestamp"]=fetch_timestamp(record["body"])
        record["status"]=fetch_status(record["body"])
        records.append(record)
        print(
            f"ID: {record['email_id']} | "
            f"Model: {record['model']} | "
            f"Status: {record['status']} | "
            f"Timestamp: {record['timestamp']}"
        )
        count+=1
    mail.close()
    mail.logout() 
    
    return records


def fetch_body(mail,eid):
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
        return False

def fetch_model(msg):
    models=[]
    for i in KNOWN_MODELS :
        if i.lower() in msg.lower():
            models.append(i)
    return models
   
def fetch_timestamp(msg):
    pattern=r"Time posted\s+([A-Z][a-z]{2}\s+\d{1,2},\s+\d{2}:\d{2}\s+UTC)"
    match=re.search(pattern,msg)
    if match:
        timestamp = match.group(1)
        return timestamp
    return "" 

def fetch_status(msg):
    pattern = r"(?:Incident status:\s*(\w+)|New incident:\s*(\w+)|Incident resolved(?!\w))"
    # print(msg)
    
    match = re.search(pattern, msg)
    if match:
        return (match.group(1) or match.group(2) or "Resolved")
    return ""
 