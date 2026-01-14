# config.py
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',  # To read unread emails & mark as read
    'https://www.googleapis.com/auth/spreadsheets'   # To write to sheets
]

# Create a new Google Sheet manually and paste its ID here
# Example URL: https://docs.google.com/spreadsheets/d/abc1234567.../edit
SPREADSHEET_ID = '1sX0m2HlJeAXXmoK_cSN_G9VKQeaXpgc1kzDNQI0x_ao' 
RANGE_NAME = 'Sheet1!A:D' # Columns A to D
CREDENTIALS_FILE = 'credentials/credentials.json'
TOKEN_FILE = 'credentials/token.json'
STATE_FILE = 'state/state.json'