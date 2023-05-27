import datetime
from django.utils import timezone
from organizers.models import Entry

WEEKDAYS = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
MONTHS = ['Январь',
          'Февраль',
          'Март',
          'Апрель',
          'Май',
          'Июнь',
          'Июль',
          'Август',
          'Сентябрь',
          'Октябрь',
          'Ноябрь',
          'Декабрь']
HUMANIZED_MONTHS = ['Января',
                    'Февраля',
                    'Марта',
                    'Апреля',
                    'Мая',
                    'Июня',
                    'Июля',
                    'Августа',
                    'Сентября',
                    'Октября',
                    'Ноября',
                    'Декабря']


class Slot:
    def __init__(self, date, price, time_comparison, is_booked, user_id=None, client_id=None):
        self.day = date.day
        self.year = date.year
        self.month = date.month
        self.month_text = HUMANIZED_MONTHS[date.month - 1]
        self.price = price
        self.weekday = date.weekday()
        self.time_comparison = time_comparison
        self.is_booked = is_booked
        self.user_id = user_id
        self.client_id = client_id


class Month:
    def __init__(self, tmp, today, entries):
        self.tmp = tmp
        self.month = MONTHS[tmp.month - 1]
        self.weeks = []
        for week_delta in range(-5, 6):
            self.add_week(self.tmp + datetime.timedelta(weeks=week_delta), today, entries)

    @staticmethod
    def get_next_sunday(date):
        weekday = date.weekday()
        return date + datetime.timedelta(days=6 - weekday)

    @staticmethod
    def get_prev_monday(date):
        weekday = date.weekday()
        return date + datetime.timedelta(days=-weekday)

    def add_week(self, date, today, entries):
        if self.get_next_sunday(date).month < self.tmp.month or self.get_prev_monday(date).month > self.tmp.month:
            return

        week_slots = []

        for weekday in range(7):
            delta = weekday - date.weekday()
            tmp_date = date + datetime.timedelta(delta)

            if tmp_date < today:
                time_comparison = 'less'
            elif tmp_date == today:
                time_comparison = 'equal'
            else:
                time_comparison = 'more'

            user_id = None
            client_id = None
            if entries.filter(date=tmp_date).exclude(client__isnull=True).exists():
                is_booked = True
                client_id = entries.filter(date=tmp_date).exclude(client__isnull=True).first().client.id
                user_id = entries.filter(date=tmp_date).exclude(client__isnull=True).first().client.user_id
            else:
                is_booked = False

            week_slots.append(Slot(tmp_date, 1000, time_comparison, is_booked, user_id=user_id, client_id=client_id))

        self.weeks.append(week_slots)


def build_calendar(platform_id):
    today = datetime.date(year=timezone.now().year, month=timezone.now().month, day=timezone.now().day)

    entries = Entry.objects.filter(platform_id=platform_id).exclude(client__isnull=True)

    months = []
    tmp = today
    for i in range(3):
        months.append(Month(tmp, today, entries))
        if tmp.month == 12:
            tmp = datetime.date(tmp.year + 1, 1, 1)
        else:
            tmp = datetime.date(tmp.year, tmp.month + 1, 1)

    return months