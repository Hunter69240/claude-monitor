import os
import imaplib
from dotenv import load_dotenv

import email
from email.policy import default
load_dotenv()
import re
import logging
logger = logging.getLogger(__name__)

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


def fetch_emails(maximum_email_id):
    logger.info("Starting email fetch")
    mail=None
    try:
        email_cred=os.getenv('GMAIL_MAIL')
        pwd_cred=os.getenv('GMAIL_PASSWORD')

        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_cred,pwd_cred)
        mail.select('inbox')

        status, message_ids = mail.uid("search",None, f'FROM "noreply@statuspage.io" UID {maximum_email_id + 1}:*')

        email_ids = message_ids[0].split()
        logger.info("Found %d matching emails", len(email_ids))
        records=[]
        for eid in email_ids: 
           
            if int(eid) > maximum_email_id:
                record={}
                record["email_id"]=eid
                record["body"] = fetch_body(mail,eid)
                if record["body"] == False:
                    logger.warning("Failed to fetch email body for ID %s", eid)
                    continue
                record["model"] = fetch_model(record["body"])
                record["occurred_at"]=fetch_timestamp(record["body"])
                record["status"]=fetch_status(record["body"])
                record["incident_id"]=fetch_incident_id(record["body"])
                    
                records.append(record)
            
        logger.info("Fetched %d email records", len(records))
        return records
    finally:
        if mail is not None:
            mail.close()
            mail.logout()
    
    

def fetch_body(mail,eid):
    try:
            # Fetch by ID
            status, msg_data = mail.uid("fetch",eid, '(RFC822)')
            if status == 'OK' and msg_data[0][1]:
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email , policy=default)
                for i in msg.walk():
                    if i.get_content_type() == "text/plain":
                        body = i.get_content() 
                return  body       
               
            else:
                return False
    except Exception:
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

    match = re.search(pattern, msg)
    if match:
        return (match.group(1) or match.group(2) or "Resolved")
    return ""

def fetch_incident_id(msg):
    pattern=r"https://stspg.io/\s*(\w+)"
    match=re.search(pattern,msg)
    if match:
        return match.group(1)
    return ""


 