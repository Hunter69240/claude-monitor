import os
import imaplib
from dotenv import load_dotenv

import email
from email.policy import default
load_dotenv()





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
        if count ==10:
            break
        record={}
        record["email_id"]=eid
        record["body"] = fetch_body(mail,eid)
        if record["body"] == False:
            continue # Later think of logging
        record["model"] = fetch_model(record["body"])
        
        records.append(record)
        count+=1
        print(records)
    mail.close()
    mail.logout() 
    
    return records


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
                print("Got body" , body)
                return  body       
               
            else:
                return False
    except Exception as e:
        print("Exception",e)
        return False

def fetch_model(msg):
    models=[]
    for i in KNOWN_MODELS :
        if i.lower() in msg.lower():
            models.append(i)
    return models
   

 