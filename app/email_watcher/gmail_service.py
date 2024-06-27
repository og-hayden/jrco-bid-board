import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from ..config import SCOPES, TOKEN_FILE
import time
import googleapiclient.errors

# Directly include the credentials in the script
CREDENTIALS_DATA = {
    "web": {
        "client_id": "216080007653-kquaa8225tme69v5gedpjc5dck0s5uub.apps.googleusercontent.com",
        "project_id": "stable-smithy-421223",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": [
            "http://localhost:8080/"
        ],
        "javascript_origins": ["http://localhost"]
    }
}

def gmail_authentication():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(CREDENTIALS_DATA, SCOPES)
            creds = flow.run_local_server(port=8080)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


def set_up_watch_request(service):
    request = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/stable-smithy-421223/topics/InboxListener'  # Replace with your topic name
    }
    while True:
        try:
            watch_response = service.users().watch(userId='me', body=request).execute()
            print(f"Watching for new emails. Expiration: {watch_response['expiration']}")
            return watch_response['historyId']
        except googleapiclient.errors.HttpError as error:
            if error.resp.status == 404:
                print("Topic not found. Please create the topic and update the code with the correct topic name.")
                raise error
            else:
                print(f"Error occurred while setting up watch request: {str(error)}")
                print("Retrying in 5 seconds...")
                time.sleep(5)

def get_email(service, user_id, email_id):
    email = service.users().messages().get(userId=user_id, id=email_id, format='full').execute()
    return email

def stop_watch_request(service):
    stop_response = service.users().stop(userId='me').execute()
    print("Stopped watching for new emails.")