import os

from celery import Celery

from archiver import (
    ALIAS,
    BitrixApp,
    GoogleSheetsApp
)
from settings import load_env_file

load_env_file("archiver/.env")

celery = Celery(__name__)
celery.conf.broker_url = os.getenv("CELERY_BROKER_URL")  # type: ignore
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")  # type: ignore
celery.conf.timezone = os.getenv("CELERY_TIMEZONE")  # type: ignore
celery.conf.broker_connection_retry = True
celery.conf.broker_connection_retry_on_startup = True

"""
Если задача периодическая:
from celery.schedules import crontab
celery.conf.beat_schedule = {
    'run-every-3-hours': {
        'task': 'process_name_task',
        'schedule': crontab(minute=0, hour='*/3') # type: ignore
    }
}
"""


@celery.task(name="process_archiver_task", acks_late=True, reject_on_worker_lost=True)
def process_archiver_task(table_key, proposal_date, deal, client, deal_id) -> dict:
    google_app = GoogleSheetsApp(table_key=table_key)
    bitrix_app = BitrixApp(os.getenv("BITRIX_WEBHOOK"))

    data = google_app.get_data()

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
                existings = bitrix_app.check_item_lists(
                    alias=ALIAS, bitrix_filter=bitrix_filter, item=item
                )
                for existing in existings:
                    bitrix_app.delete_item(str(existing["ID"]))
                bitrix_app.add_item(alias=ALIAS, item=item)
            except:
                pass
    return {"Status": "Success"}
