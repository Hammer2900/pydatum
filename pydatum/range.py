from datetime import datetime, timedelta

PERIOD = {
    'minute': timedelta(minutes=1),
    'hour': timedelta(hours=1),
    'day': timedelta(days=1),
    'week': timedelta(days=7),
    'month': timedelta(days=31)
}


class DateRange:
    """ Represents a date range """

    def __init__(self, start: datetime = None, end: datetime = None):
        self.start: datetime = start
        self.end: datetime = end

        self.turn_lock = self.calculate_turn_lock()
        self.turn_delta = self.calculate_turn_delta()

    def calculate_turn_lock(self):
        return '__ge__' if self.end > self.start else '__le__'

    def calculate_turn_delta(self):
        return '__add__' if self.end > self.start else '__sub__'

    def calculate_lock(self, temp_date, end_date):
        return getattr(temp_date, self.turn_lock)(end_date)

    def calculate_delta(self, temp_date, delta):
        return getattr(temp_date, self.turn_delta)(delta)

    def split_by(self, period='minute'):
        delta = PERIOD.get(period, 'minute')
        temp_date = self.start
        while not self.calculate_lock(temp_date, self.end):
            yield temp_date
            temp_date = self.calculate_delta(temp_date, delta)
