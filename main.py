import os
from datetime import datetime

from dotenv import load_dotenv

from src.alias import ALIAS
from src.bitrix_client import BitrixApp
from src.google_client import GoogleSheetsApp

if __name__ == "__main__":
    load_dotenv(".env")
    google_app = GoogleSheetsApp(os.getenv("GOOGLE_SHEETS_URL"))
    bitrix_app = BitrixApp(os.getenv("BITRIX_WEBHOOK"))

    data = google_app.get_data()

    deal = "deal"
    proposal_date = datetime.now()
    client = "client"
    deal_id = "1"

    extra = {
        "Сделка": deal,
        "Дата предложения": proposal_date,
        "Клиент": client,
        "ID сделки": deal_id,
    }

    for item in data:
        if item.get("Наименование МТР"):
            try:
                bitrix_filter = ["ID сделки", "Наименование МТР", "№"]
                item.update(extra)
                bitrix_app.check_item_lists(alias=ALIAS, bitrix_filter=bitrix_filter, item=item)
                bitrix_app.add_item(alias=ALIAS, item=item)
            except:
                pass
