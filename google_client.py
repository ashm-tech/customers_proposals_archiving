import gspread
from google.oauth2.credentials import Credentials


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


class GoogleSheetsApp:
    def __init__(self, table_key):
        self.credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
        self.g_client = gspread.authorize(self.credentials)
        self.table = self.g_client.open_by_key(table_key)

    def get_data(self):
        entities = []
        sheet = self.table.get_worksheet(0)
        sheet_data = sheet.get_all_values()
        headers = sheet_data[0]

        for row in sheet_data[1:]:
            entity = {}
            for idx, value in enumerate(row):
                entity[headers[idx]] = value
            entities.append(entity)

        return entities
