# src/sheets_service.py
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from bs4 import BeautifulSoup
import config

def get_sheets_service():
    """Builds the Sheets API service using existing token."""
    creds = Credentials.from_authorized_user_file(config.TOKEN_FILE, config.SCOPES)
    return build('sheets', 'v4', credentials=creds)

def append_to_sheet(service, data):
    """Appends a row of data to the configured spreadsheet."""
    # Convert email body to plain text
    plain_content = BeautifulSoup(data['Content'], 'html.parser').get_text()

    # Row to append
    values = [[
        data['From'],
        data['Subject'],
        data['Date'],
        plain_content
    ]]

    # Check if sheet has data already
    sheet_data = service.spreadsheets().values().get(
        spreadsheetId=config.SPREADSHEET_ID,
        range=config.RANGE_NAME
    ).execute()

    if not sheet_data.get('values'):
        # Add headers if sheet is empty
        headers = [['From', 'Subject', 'Date', 'Content']]
        service.spreadsheets().values().append(
            spreadsheetId=config.SPREADSHEET_ID,
            range=config.RANGE_NAME,
            valueInputOption='RAW',
            body={'values': headers}
        ).execute()

    # Append the actual email row
    service.spreadsheets().values().append(
        spreadsheetId=config.SPREADSHEET_ID,
        range=config.RANGE_NAME,
        valueInputOption='RAW',
        body={'values': values}
    ).execute()

    # Auto-fit columns 
    service.spreadsheets().batchUpdate(
        spreadsheetId=config.SPREADSHEET_ID,
        body={
            "requests": [
                {
                    "autoResizeDimensions": {
                        "dimensions": {
                            "sheetId": 0,       # first sheet
                            "dimension": "COLUMNS",
                            "startIndex": 0,
                            "endIndex": 4       # total 4 columns
                        }
                    }
                }
            ]
        }
    ).execute()
