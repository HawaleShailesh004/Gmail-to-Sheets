# src/gmail_service.py
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import config

def authenticate_gmail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists(config.TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(config.TOKEN_FILE, config.SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.CREDENTIALS_FILE, config.SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(config.TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def fetch_unread_emails(service):
    """Fetch list of unread messages from Inbox."""
    # q='is:unread in:inbox' filters strictly for unread inbox emails
    results = service.users().messages().list(userId='me', q='is:unread in:inbox', maxResults=5).execute()
    messages = results.get('messages', [])
    return messages

def get_email_details(service, msg_id):
    """Fetch full details of a specific email."""
    return service.users().messages().get(userId='me', id=msg_id, format='full').execute()

def mark_as_read(service, msg_id):
    """Remove the UNREAD label from the email."""
    service.users().messages().modify(
        userId='me', 
        id=msg_id, 
        body={'removeLabelIds': ['UNREAD']}
    ).execute()