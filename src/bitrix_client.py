import os
import uuid

from fast_bitrix24 import Bitrix


class BitrixApp:
    def __init__(self, webhook):
        self.bitrix = Bitrix(webhook)

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
