from datetime import datetime, timedelta
from time import mktime

import settings


class DateTimeConverter:
    @classmethod
    def from_timestamp_to_date(cls, timestamp: int, as_string: bool = False):
        date = datetime.fromtimestamp(timestamp)
        return cls._to_string(date) if as_string else date

    @staticmethod
    def from_date_to_timestamp(date: datetime):
        return int(mktime(date.timetuple()))

    @staticmethod
    def from_str_to_date(date_string: str):
        return datetime.strptime(date_string, settings.DATE_FORMAT)

    @classmethod
    def date_from_now(cls, days: int, as_string: bool = False):
        date = datetime.now() - timedelta(days=days)
        return cls._to_string(date) if as_string else date

    @staticmethod
    def _to_string(date: datetime):
        return date.strftime(settings.DATE_FORMAT)
