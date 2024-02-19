import os
import uuid

from fast_bitrix24 import Bitrix


class BitrixApp:
    def __init__(self, webhook):
        self.bitrix = Bitrix(webhook)

    def get_all_items(self) -> list:
        """Return all items from the list"""
        params = {
            "IBLOCK_TYPE_ID": "lists",
            "IBLOCK_ID": os.getenv("LIST_ID"),
        }
        bitrix_list = self.bitrix.get_all("lists.element.get", params)
        return bitrix_list

    def add_item(self, alias: dict, item: dict):
        """
        Adds an item to the list
        :param alias: alias from item fields to bitrix fields
        :param item: item to add
        """
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

    def check_item_lists(self, alias: dict, bitrix_filter: list, item: dict) -> list:
        """
        Checks if item is in lists
        :param alias: alias from item fields to bitrix fields
        :param bitrix_filter: fields of item for searching
        :param item: item to check
        """
        fields = {}
        for key, value in alias.items():
            if key in bitrix_filter:
                try:
                    fields[value] = item[key]
                except KeyError:
                    pass

        results = self.bitrix.get_all(
            "lists.element.get",
            {
                "IBLOCK_TYPE_ID": "lists",
                "IBLOCK_ID": os.getenv("LIST_ID"),
                "FILTER": fields,
            },
        )

        return results

    def delete_item(self, item_ids):
        for item_id in item_ids:
            self.bitrix.call(
                "lists.element.delete",
                {
                    "IBLOCK_TYPE_ID": "lists",
                    "IBLOCK_ID": os.getenv("LIST_ID"),
                    "ELEMENT_ID": item_id,
                },
            )
