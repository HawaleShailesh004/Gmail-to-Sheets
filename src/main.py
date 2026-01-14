import os
import json
import config
from datetime import datetime # <--- NEW IMPORT
from src import gmail_service, sheets_service, email_parser

def log(message):
    """Helper for Bonus: Logging with Timestamps"""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {message}")

def load_processed_ids():
    """Load the list of already processed message IDs."""
    if not os.path.exists(config.STATE_FILE):
        return set()
    try:
        with open(config.STATE_FILE, 'r') as f:
            data = f.read().strip()
            if not data:
                return set()
            return set(json.loads(data))
    except json.JSONDecodeError:
        log("⚠️ State file corrupted. Resetting...")
        return set()

def save_processed_id(msg_id, current_list):
    """Update the state file with the new ID."""
    current_list.add(msg_id)
    os.makedirs(os.path.dirname(config.STATE_FILE), exist_ok=True)
    with open(config.STATE_FILE, 'w') as f:
        json.dump(list(current_list), f)

def main():
    log("🚀 Starting Gmail to Sheets Automation...")
    log("Fetching first 5 Unread emails from Inbox...")
    # 1. Authenticate
    gmail = gmail_service.authenticate_gmail()
    sheets = sheets_service.get_sheets_service()
    
    # 2. Load State
    processed_ids = load_processed_ids()
    
    # 3. Fetch Unread Emails
    messages = gmail_service.fetch_unread_emails(gmail)
    
    if not messages:
        log("✅ No new unread emails found.")
        return

    log(f"📥 Found {len(messages)} unread emails. Processing...")

    for msg in messages:
        msg_id = msg['id']
        
        if msg_id in processed_ids:
            log(f"⚠️ Skipping duplicate (locally tracked): {msg_id}")
            continue

        try:
            # 4. Parse Email
            full_msg = gmail_service.get_email_details(gmail, msg_id)
            email_data = email_parser.parse_email(full_msg, full_msg['internalDate'])
            
            # 5. Append to Sheets
            sheets_service.append_to_sheet(sheets, email_data)
            log(f"📝 Logged: {email_data['Subject']}")
            
            # 6. Mark as Read
            gmail_service.mark_as_read(gmail, msg_id)
            
            # 7. Update Local State
            save_processed_id(msg_id, processed_ids)
            
        except Exception as e:
            log(f"❌ Error processing message {msg_id}: {e}")

    log("🎉 All tasks completed successfully.")

if __name__ == '__main__':
    main()