# src/email_parser.py
import base64
from bs4 import BeautifulSoup
from datetime import datetime

def parse_email(msg_payload, msg_internal_date):
    """Extracts required fields from email payload."""
    headers = msg_payload.get('payload', {}).get('headers', [])
    
    subject = "No Subject"
    sender = "Unknown"
    
    for header in headers:
        if header['name'] == 'Subject':
            subject = header['value']
        if header['name'] == 'From':
            sender = header['value']

    # Handle Date (Convert internal timestamp to readable format)
    # internalDate is in milliseconds
    date_obj = datetime.fromtimestamp(int(msg_internal_date) / 1000)
    date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')

    # Handle Body (Plain Text or HTML)
    body = ""
    parts = msg_payload.get('payload', {}).get('parts', [])
    
    # If the email has no parts (simple plain text)
    if not parts:
        data = msg_payload.get('payload', {}).get('body', {}).get('data')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8')
    else:
        # Prefer plain text if available
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
        # Fallback to HTML if no plain text
        if not body:
            for part in parts:
                if part['mimeType'] == 'text/html':
                    data = part['body'].get('data')
                    if data:
                        html_content = base64.urlsafe_b64decode(data).decode('utf-8')
                        soup = BeautifulSoup(html_content, 'html.parser')
                        body = soup.get_text()

    if body:
        clean_body = " ".join(body.split())
    else:
        clean_body = ""
    return {
        "From": sender,
        "Subject": subject,
        "Date": date_str,
        "Content": clean_body
    }