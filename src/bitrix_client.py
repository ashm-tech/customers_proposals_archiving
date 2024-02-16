import os
import uuid

from fast_bitrix24 import Bitrix

from src.alias import ALIAS


class BitrixApp:
    def __init__(self):
        self.bitrix = Bitrix(os.getenv("BITRIX_WEBHOOK"))

    def get_all_items(self):
        params = {
            "IBLOCK_TYPE_ID": "lists",
            "IBLOCK_ID": os.getenv("LIST_ID"),
        }
        bitrix_list = self.bitrix.get_all("lists.element.get", params)
        return bitrix_list

    def add_item(self, alias, item):
        fields = {}
        for key, value in alias.items():
            try:
                fields[value] = item[key]
            except KeyError:
                pass
        params = {
            "IBLOCK_TYPE_ID": "lists",
            "IBLOCK_ID": os.getenv("LIST_ID"),
            "ELEMENT_CODE": uuid.uuid4(),
            "FIELDS": fields,
        }
        result = self.bitrix.call("lists.element.add", params)
        return result


if __name__ == "__main__":
    test_item = {
        "Наименование МТР": "NAMES",
        "Менеджер": "PROPERTY_109",
        "Базис поставки": "PROPERTY_111",
        "ЕНС": 113,
        "ГОСТ": "PROPERTY_117",
        "Изготовитель": "PROPERTY_119",
        "ЕИ": "PROPERTY_121",
        "Количество": 141,
        "№": 125,
        "Цена за шт, евро": "127|EUR",
        "сть-ть евро": "129|EUR",
        "срок": "PROPERTY_131",
        "Сделка": "PROPERTY_133",
        "Дата предложения": "16.02.2024 22:46:00",
        "Клиент": "PROPERTY_137",
        "ID сделки": 139,
    }
    bitrix = BitrixApp()
    print(bitrix.add_item(alias=ALIAS, item=test_item))
