import gspread


class GoogleSheetsApp:
    def __init__(self, table_key):
        self.g_client = gspread.service_account(filename="archiver/credentials.json")
        self.table = self.g_client.open_by_key(table_key)

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
