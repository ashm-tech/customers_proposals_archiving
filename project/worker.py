import os
from datetime import datetime

from celery import Celery

from settings import load_env_file
from archiver.alias import ALIAS
from archiver.bitrix_client import BitrixApp
from archiver.google_client import GoogleSheetsApp

load_env_file()

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


@celery.task(
    name='process_archiver_task',
    acks_late=True,
    reject_on_worker_lost=True
)
def process_archiver_task() -> dict:
    """
    Логика таски
    """
    google_app = GoogleSheetsApp(os.getenv("GOOGLE_SHEETS_KEY"))
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
                bitrix_app.check_item_lists(
                    alias=ALIAS, bitrix_filter=bitrix_filter, item=item
                )
                bitrix_app.add_item(alias=ALIAS, item=item)
            except:
                pass
    return {
        'Status': 'Success'
    }
