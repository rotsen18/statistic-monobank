from datetime import datetime, timedelta
from time import mktime

import settings


class DateTimeConverter:
    @staticmethod
    def from_timestamp_to_date(timestamp: int):
        return datetime.fromtimestamp(timestamp)

    @staticmethod
    def from_date_to_timestamp(date: datetime):
        return int(mktime(date.timetuple()))

    @staticmethod
    def from_str_to_date(date_string: str):
        return datetime.strptime(date_string, settings.DATE_FORMAT)

    @staticmethod
    def date_from_now(days: int):
        return datetime.now() - timedelta(days=days)
