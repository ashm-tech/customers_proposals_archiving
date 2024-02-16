import gspread
from google.oauth2.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class GoogleSheetsApp:
    def __init__(self, table_url):
        self.credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
        self.g_client = gspread.authorize(self.credentials)
        self.table = self.g_client.open_by_url(table_url)

    def get_data(self):
        entities = []
        sheet = self.table.sheet1
        sheet_data = sheet.get_all_values()
        headers = sheet_data[0]

        for row in sheet_data:
            entity = {}
            for idx, value in enumerate(row):
                entity[headers[idx]] = value
            entities.append(entity)

        return entities
