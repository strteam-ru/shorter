from datetime import datetime, timedelta

from shorter import settings
from ..logger import logger
from ..models import Links


class Hits:

    @staticmethod
    def run_hits():
        Hits.clear_old_records()
        return

    @staticmethod
    def clear_old_records():
        max_record_time = datetime.now() - timedelta(seconds=int(settings.LINK_TTL))
        Links.objects.filter(created__lte=max_record_time).delete()
        logger.info('DB clear complete')
        return
