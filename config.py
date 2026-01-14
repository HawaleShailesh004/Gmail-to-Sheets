# config.py
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',  # To read unread emails & mark as read
    'https://www.googleapis.com/auth/spreadsheets'   # To write to sheets
]


SPREADSHEET_ID = 'PUT SPREADSHEET ID HERE' 
RANGE_NAME = 'Sheet1!A:D' # Columns A to D
CREDENTIALS_FILE = 'credentials/credentials.json'
TOKEN_FILE = 'credentials/token.json'
STATE_FILE = 'state/state.json'