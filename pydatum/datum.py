"""
Datetime utilities similar to Joda Time or Calendar in Java 
See https://pymotw.com/2/datetime/ for more arithmetic.
"""
import calendar
import re
from datetime import date, datetime, time, timedelta
# from logging import DEBUG, log

from dateutil.relativedelta import relativedelta

ISO_DATE_FORMAT = "%Y-%m-%d"
ISO_LONG_FORMAT = "%Y-%m-%dT%H:%M:%S"
ISO_FULL_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

PERIODS = {
    'second': dict(microsecond=0),
    'minute': dict(microsecond=0, second=0),
    'hour': dict(microsecond=0, second=0, minute=0),
    'day': dict(microsecond=0, second=0, minute=0, hour=0, ),
    'month': dict(microsecond=0, second=0, minute=0, hour=0, day=1),
    'year': dict(microsecond=0, second=0, minute=0, hour=0, day=1, month=1),
}


class Datum:
    """ Encapsulates datetime value and provides operations on top of it """

    def __init__(self):
        self.value: datetime = datetime.now()

    @staticmethod
    def parse(value: str):
        """ Parse date string. Currently only ISO strings supported yyyy-mm-dd. """
        result = Datum()

        if value.isdigit():
            result.from_timestamp_date_string(value)
        elif isinstance(value, datetime):
            result.from_datetime(value)
        else:
            result.from_iso_date_string(value)

        return result

    # //////////////////////// Arithmetic ////////////////////////

    def truncate(self, truncate_to='day'):
        self.value = self.value.replace(**PERIODS[truncate_to])
        return self.value

    def add_days(self, days: int) -> datetime:
        """ Adds days """
        self.value = self.value + relativedelta(days=days)
        return self.value

    def add_months(self, value: int) -> datetime:
        """ Add a number of months to the given date """
        self.value = self.value + relativedelta(months=value)
        return self.value

    def add_hours(self, value: int) -> datetime:
        """ Add a number of months to the given date """
        self.value = self.value + relativedelta(hour=value)
        return self.value

    def add_minutes(self, value: int) -> datetime:
        """ Add a number of months to the given date """
        self.value = self.value + relativedelta(minutes=value)
        return self.value

    def substract_days(self, days: int) -> datetime:
        """ Substract days """
        self.value = self.value - relativedelta(days=days)
        return self.value

    def substract_months(self, value: int) -> datetime:
        """ Substract a number of months to the given date """
        self.value = self.value - relativedelta(months=value)
        return self.value

    def substract_hours(self, value: int) -> datetime:
        """ Substract a number of months to the given date """
        self.value = self.value - relativedelta(hour=value)
        return self.value

    def substract_minutes(self, value: int) -> datetime:
        """ Substract a number of months to the given date """
        self.value = self.value - relativedelta(minutes=value)
        return self.value

    def subtract_weeks(self, weeks: int) -> datetime:
        """ Subtracts number of weeks from the current value """
        self.value = self.value - timedelta(weeks=weeks)
        return self.value

    def clone(self):
        """ Cretes a copy """
        copy = Datum()
        copy.from_datetime(self.value)
        return copy

    @property
    def date(self) -> date:
        """ Returns the date value """
        return self.value.date()

    @property
    def time(self) -> time:
        """ The time value """
        return self.value.time()

    @property
    def datetime(self) -> datetime:
        """ The datetime value. """
        return self.value

    @property
    def epoch(self) -> int:
        """ The timestamp value. """
        return int(self.value.strftime('%s'))

    @property
    def epoch_miliseconds(self) -> int:
        """ The timestamp value with miliseconds. """
        return int(self.value.strftime('%s')) * 1000

    def from_date(self, value: date) -> datetime:
        """ Initializes from the given date value """
        assert isinstance(value, date)

        self.value = datetime(value.year, value.month, value.day)
        return self.value

    def from_datetime(self, value: datetime) -> datetime:
        assert isinstance(value, datetime)

        self.value = value
        return self.value

    def from_iso_long_date(self, date_str: str) -> datetime:
        """ Parse ISO date string (YYYY-MM-DDTHH:mm:ss) """
        assert isinstance(date_str, str)
        assert len(date_str) == 19

        self.value = datetime.strptime(date_str, ISO_LONG_FORMAT)
        return self.value

    def from_iso_date_string(self, date_str: str) -> datetime:
        """ Parse ISO date string (YYYY-MM-DD) """
        assert isinstance(date_str, str)

        self.value = datetime.strptime(date_str, ISO_DATE_FORMAT)
        return self.value

    def from_timestamp_date_string(self, date_str: str) -> datetime:
        """ Parse timestamp date string (1560718800) """
        assert isinstance(date_str, str)

        self.value = datetime.fromtimestamp(int(date_str))
        return self.value

    def get_day(self) -> int:
        """ Returns the day value """
        return self.value.day

    def get_day_name(self) -> str:
        """ Returns the day name """
        weekday = self.value.isoweekday() - 1
        return calendar.day_name[weekday]

    def get_iso_date_string(self):
        return self.to_iso_date_string()

    def to_iso_date_string(self):
        """ Gets the iso string representation of the given date """
        return self.value.strftime(ISO_DATE_FORMAT)

    def get_iso_string(self) -> str:
        return self.to_iso_string()

    def to_iso_string(self) -> str:
        """ Returns full ISO string for the given date """
        assert isinstance(self.value, datetime)
        return datetime.isoformat(self.value)

    def get_month(self) -> int:
        """ Returns the year """
        return self.value.month

    def get_year(self) -> int:
        """ Returns the year """
        return self.value.year

    # /////////////////////////// Slice ///////////////////////////

    def start_of_day(self) -> datetime:
        """ Returns start of day """
        self.value = datetime(self.value.year, self.value.month, self.value.day)
        return self.value

    def end_of_day(self) -> datetime:
        """ End of day """
        self.value = datetime(self.value.year, self.value.month, self.value.day, 23, 59, 59)
        return self.value

    def start_of_month(self):
        """ Return start month date """
        self.start_of_day()
        self.value = self.value.replace(day=1)
        return self.value

    def end_of_month(self) -> datetime:
        """ Provides end of the month for the given date """
        # Increase month by 1,
        result = self.value + relativedelta(months=1)
        # take the 1st day of the (next) month,
        result = result.replace(day=1)
        # subtract one day
        result = result - relativedelta(days=1)
        self.value = result
        return self.value

    def begin_of_week(self) -> datetime:
        """ Set the value to beginning of the week """
        self.value = self.value - timedelta(days=self.value.weekday())
        return self.value

    def yesterday(self) -> datetime:
        """ Set the value to yesterday """
        self.value = datetime.today() - timedelta(days=1)
        return self.value

    # ////////////////////////// Checks //////////////////////////

    def is_end_of_month(self) -> bool:
        """ Checks if the date is at the end of the month """
        end_of_month = Datum()
        # get_end_of_month(value)
        end_of_month.end_of_month()
        return self.value == end_of_month.value

    def is_weekday(self, date):
        """ Checks if the date provided as an arguement is a weekday or not """
        return True if date.weekday() in range(0, 5) else False

    def set_day(self, day: int) -> datetime:
        """ Sets the day value """
        self.value = self.value.replace(day=day)
        return self.value

    def set_value(self, value: datetime):
        """ Sets the current value """
        assert isinstance(value, datetime)

        self.value = value

    def to_short_time_string(self) -> str:
        """ Return the iso time string only. i.e. 22:33 """
        hour = self.time.hour
        minute = self.time.minute
        return f"{hour:02}:{minute:02}"

    def to_long_time_string(self) -> str:
        """ Return the iso time string only. i.e. """
        hour = self.time.hour
        minute = self.time.minute
        second = self.time.second
        return f"{hour:02}:{minute:02}:{second:02}"

    def to_datetime_string(self) -> str:
        """ Returns a human-readable string representation with iso date and time
        Example: 2018-12-06 12:32:56
        """
        date_display = self.to_iso_date_string()
        time_display = self.to_long_time_string()
        return f"{date_display} {time_display}"

    def to_long_datetime_string(self) -> str:
        """ Returns the long date/time string
        Example: 2018-12-06 12:34
        """
        date_display = self.to_iso_date_string()
        time_display = self.to_short_time_string()
        return f"{date_display} {time_display}"

    def today(self) -> datetime:
        """ Returns today (date only) as datetime """
        self.value = datetime.combine(datetime.today().date(), time.min)
        return self.value

    # ///////////////////////// Iterators /////////////////////////

    def day_range_weekday(self, start, end):
        """
        Returns a generator that can be used to iterate over
        the weekdays in the range start to end-1
        """
        if start > end:
            return
        while not start == end:
            if self.is_weekday(start):
                yield start
            start += timedelta(days=1)

    def __repr__(self):
        """ string representation """
        datetime_str = self.to_datetime_string()

        return f"{datetime_str}"


if __name__ == '__main__':
    a = Datum.parse('1560718800')
    a.add_months(1)
    # a.add_days(1)
    # a.add_hours(1)
    # a.add_minutes(40)
    # a.substract_days(1)
    print('[√]: ', a)
    print('[√]: ', a.epoch_miliseconds)
