# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from suntime import Sun
import csv
import sys
from os import path
import io
import yaml


class jewishcal():
    def __init__(self):

        PROJ_PATH = path.sep.join(__file__.split(path.sep)[:-2])
        DATA_PATH = path.join(
            PROJ_PATH, 'hebwatch/hebrew-special-numbers-default.yml')
        self.specialnumbers = yaml.safe_load(
            io.open(DATA_PATH, encoding='utf8'))

        MAP = (
            (1, u'א'),
            (2, u'ב'),
            (3, u'ג'),
            (4, u'ד'),
            (5, u'ה'),
            (6, u'ו'),
            (7, u'ז'),
            (8, u'ח'),
            (9, u'ט'),
            (10, u'י'),
            (20, u'כ'),
            (30, u'ל'),
            (40, u'מ'),
            (50, u'נ'),
            (60, u'ס'),
            (70, u'ע'),
            (80, u'פ'),
            (90, u'צ'),
            (100, u'ק'),
            (200, u'ר'),
            (300, u'ש'),
            (400, u'ת'),
            (500, u'ך'),
            (600, u'ם'),
            (700, u'ן'),
            (800, u'ף'),
            (900, u'ץ')
        )
        self.MAP_DICT = dict([(k, v) for v, k in MAP])
        self.GERESH = set(("'", '׳'))

    def gematria_to_int(self, string):
        res = 0
        for i, char in enumerate(string):
            if char in self.GERESH and i < len(string)-1:
                res *= 1000
            if char in self.MAP_DICT:
                res += self.MAP_DICT[char]
        return res

    # adapted from hebrew-special-numbers documentation
    def int_to_gematria(self, num, gershayim=True):
        """convert integers between 1 an 999 to Hebrew numerals.

              - set gershayim flag to False to ommit gershayim
        """
        # 1. Lookup in specials
        if num in self.specialnumbers['specials']:
            retval = self.specialnumbers['specials'][num]
            return self._add_gershayim(retval) if gershayim else retval

        # 2. Generate numeral normally
        parts = []
        rest = str(num)
        while rest:
            digit = int(rest[0])
            rest = rest[1:]
            if digit == 0:
                continue
            power = 10 ** len(rest)
            parts.append(self.specialnumbers['numerals'][power * digit])
        retval = ''.join(parts)
        # 3. Add gershayim
        return self._add_gershayim(retval) if gershayim else retval

    def _add_gershayim(self, s):
        if len(s) == 1:
            s += self.specialnumbers['separators']['geresh']
        else:
            s = ''.join([
                s[:-1],
                self.specialnumbers['separators']['gershayim'],
                s[-1:]
            ])
        return s

    def get_weekday_from_absdate(self, absdate):
        return absdate % 7

    def leap_gregorian(self, year):
        if ((year % 4) == 0) and \
            ((year % 400) != 100) and \
            ((year % 400) != 200) and \
                ((year % 400) != 300):
            return True
        else:
            return False

    def last_day_of_gregorian_month(self, month, year):
        if self.leap_gregorian(year) == True and month == 2:
            return 29
        else:
            lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            return lengths[month-1]

    def hebrew_leap(self, year):
        if ((((year*7)+1) % 19) < 7):
            return True
        else:
            return False

    def hebrew_year_months(self, year):
        if self.hebrew_leap(year):
            return 13
        else:
            return 12

    def _hebrew_calendar_elapsed_days(self, year):
        value = 235 * ((year-1) // 19)
        monthsElapsed = value

        value = 12 * ((year-1) % 19)
        monthsElapsed += value

        value = ((((year-1) % 19) * 7) + 1) // 19
        monthsElapsed += value

        partsElapsed = (((monthsElapsed % 1080) * 793) + 204)
        hoursElapsed = (5 +
                        (monthsElapsed * 12) +
                        ((monthsElapsed // 1080) * 793) +
                        (partsElapsed // 1080))

        day = 1 + (29 * monthsElapsed) + (hoursElapsed//24)

        parts = ((hoursElapsed % 24) * 1080) + \
                (partsElapsed % 1080)

        if ((parts >= 19440) or
            (((day % 7) == 2) and
            (parts >= 9924) and
            (not self.hebrew_leap(year))) or
            (((day % 7) == 1) and
            (parts >= 16789) and
                (self.hebrew_leap(year-1)))):
            alternativeDay = day+1
        else:
            alternativeDay = day

        if (((alternativeDay % 7) == 0) or
            ((alternativeDay % 7) == 3) or
                ((alternativeDay % 7) == 5)):
            alternativeDay += 1

        return alternativeDay

    def days_in_hebrew_year(self, year):
        return (self._hebrew_calendar_elapsed_days(year+1) -
                self._hebrew_calendar_elapsed_days(year))

    def _long_heshvan(self, year):
        if ((self.days_in_hebrew_year(year) % 10) == 5):
            return True
        else:
            return False

    def _short_kislev(self, year):
        if ((self.days_in_hebrew_year(year) % 10) == 3):
            return True
        else:
            return False

    def hebrew_month_days(self, year, month):
        if ((month == 2) or
            (month == 4) or
            (month == 6) or
            (month == 10) or
                (month == 13)):
            return 29
        if ((month == 12) and (not self.hebrew_leap(year))):
            return 29
        if ((month == 8) and (not self._long_heshvan(year))):
            return 29
        if ((month == 9) and (self._short_kislev(year))):
            return 29
        return 30

    def hebrew_to_absdate(self, year, month, day):
        value = day
        returnValue = value

        if month < 7:
            for m in range(7, self.hebrew_year_months(year)+1):
                value = self.hebrew_month_days(year, m)
                returnValue += value
            for m in range(1, month):
                value = self.hebrew_month_days(year, m)
                returnValue += value
        else:
            for m in range(7, month):
                value = self.hebrew_month_days(year, m)
                returnValue += value

        value = self._hebrew_calendar_elapsed_days(year)
        returnValue += value

        value = 1373429
        returnValue -= value

        return returnValue

    def absdate_to_hebrew(self, absdate):  # year, month, day
        approx = (absdate+1373429) // 366

        y = approx
        while 1:
            temp = self.hebrew_to_absdate(y+1, 7, 1)
            if absdate < temp:
                break
            y += 1
        year = y

        temp = self.hebrew_to_absdate(year, 1, 1)
        if absdate < temp:
            start = 7
        else:
            start = 1

        m = start
        while 1:
            temp = self.hebrew_to_absdate(
                year, m, self.hebrew_month_days(year, m))
            if absdate <= temp:
                break
            m += 1
        month = m

        temp = self.hebrew_to_absdate(year, month, 1)
        day = absdate-temp+1

        return (year, month, day)

    def gregorian_to_absdate(self, year, month, day):
        value = day
        returnValue = value

        for m in range(1, month):
            value = self.last_day_of_gregorian_month(m, year)
            returnValue += value

        value = (365 * (year-1))
        returnValue += value

        value = ((year-1) // 4)
        returnValue += value

        value = ((year-1) // 100)
        returnValue -= value

        value = ((year-1) // 400)
        returnValue += value

        return returnValue

    def absdate_to_gregorian(self, absdate):
        approx = absdate // 366

        y = approx
        while 1:
            temp = self.gregorian_to_absdate(y+1, 1, 1)
            if (absdate < temp):
                break
            y += 1
        year = y

        m = 1
        while 1:
            temp = self.gregorian_to_absdate(
                year, m, self.last_day_of_gregorian_month(m, year))
            if (absdate <= temp):
                break
            m += 1
        month = m

        temp = self.gregorian_to_absdate(year, month, 1)
        day = absdate-temp+1

        return (year, month, day)

    def hebrew_date_from_num(self, year, month, day):
        if month == 1:
            heb_month = "ניסן"
        elif month == 2:
            heb_month = "אייר"
        elif month == 3:
            heb_month = "סיוון"
        elif month == 4:
            heb_month = "תמוז"
        elif month == 5:
            heb_month = "אב"
        elif month == 6:
            heb_month = "אלול"
        elif month == 7:
            heb_month = "תשרי"
        elif month == 8:
            heb_month = "חשוון"
        elif month == 9:
            heb_month = "כסלו"
        elif month == 10:
            heb_month = "טבת"
        elif month == 11:
            heb_month = "שבט"
        elif month == 12:
            if self.hebrew_leap(year):
                heb_month = "אדר א"
            else:
                heb_month = "אדר"

        elif month == 13:
            heb_month = "אדר ב"

        heb_list = ['',
                    'א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'יא', 'יב', 'יג', 'יד',
                    'טו', 'טז', 'יז', 'יח', 'יט', 'כ', 'כא', 'כב', 'כג', 'כד', 'כה', 'כו', 'כז',
                    'כח', 'כט', 'ל', 'לא'
                    ]
        heb_day = heb_list[day]

        heb_year_h = self.int_to_gematria(year % 1000)
        heb_year_t = self.int_to_gematria(int(str(year)[0]))
        heb_year = f'{heb_year_t}{heb_year_h}'

        return (f'{heb_day} {heb_month} {heb_year}')


project_path = path.sep.join(__file__.split(path.sep)[:-2])
cities_path = path.join(project_path, 'hebwatch/cities.csv')


def get_coords(city):
    try:
        with open(cities_path, 'r', encoding="utf8") as file:
            reader = csv.reader(file)
            lat = 0
            lon = 0
            for row in reader:
                if row[0] == city:
                    lat = float(row[1])
                    lon = float(row[2])
            if lat != 0 or lon != 0:
                return lat, lon
            else:
                sys.exit("city is not found")

    except:
        sys.exit("cities.csv file is required for this library")


class watch(jewishcal):

    def __init__(self, city, current_time=None):

        super().__init__()

        self.current_time = datetime.now() if current_time is None else current_time

        self.lat, self.lon = get_coords(city)
        sun = Sun(self.lat, self.lon)

        self.city = city
        self.sunrise = (sun.get_sunrise_time(date=self.current_time) + timedelta(hours=watch.utc_israel())).replace(tzinfo=None)
        self.sunset = (sun.get_sunset_time(date=self.current_time) + timedelta(hours=watch.utc_israel())).replace(tzinfo=None)
        self.yt_sunset = (sun.get_sunset_time(date=self.current_time + timedelta(days=-1))+timedelta(hours=watch.utc_israel())).replace(tzinfo=None)
        self.nd_sunrise = (sun.get_sunrise_time(date=self.current_time + timedelta(days=1))+timedelta(hours=watch.utc_israel())).replace(tzinfo=None)
        self.night_len = None
        self.curr_len = None
        self.day_len = None
        self.night_second_len = None
        self.night_hour_len = None
        self.day_second_len = None
        self.day_hour_len = None

    def dec_to_hourformat(self, decimal):
        H_raw = decimal
        H, M_raw = int(H_raw), (H_raw-int(H_raw))*60
        M, S_raw = int(M_raw), (M_raw-int(M_raw))*60
        S, MS = int(S_raw), int((S_raw-int(S_raw))*100)
        hour_format = datetime.strptime(
            f'{H}:{M}:{S}', "%H:%M:%S").strftime("%H:%M:%S")

        return hour_format

    def utc_israel(now=datetime.now()):
        y, m, d, hh, mm, ss, wd, yd, __ = now.timetuple()
        october_last_day = datetime(y, 10, 31, 2, 0, 0)
        if october_last_day.weekday() != 6:
            for i in range(31, 23, -1):
                cheack = datetime(y, 10, i, 2, 0, 0)
                if cheack.weekday() == 6:
                    october_last_sunday = cheack
                    break

        # last day of march -> 6 - 2
        march_last_day = datetime(y, 3, 31, 2, 0, 0)
        if march_last_day.weekday() != 6:
            for i in range(31, 23, -1):
                cheack = datetime(y, 3, i, 2, 0, 0)
                if cheack.weekday() == 6:
                    cheack = datetime(y, 3, i-2, 2, 0, 0)
                    march_last_friday = cheack
                    break

        if now > march_last_friday and now < october_last_sunday:
            utc_offset = 3
        else:
            utc_offset = 2

        return utc_offset

    def day_relativeHour(self):
        """
        calculate the relative hour for the day    

        current_time = get datetime obj
        """

        self.day_len = (self.sunset - self.sunrise).seconds
        self.curr_len = (self.current_time - self.sunrise).seconds

        self.day_hour_len = (self.day_len/12/60)
        self.day_second_len = (self.day_hour_len/60)

        temp_hour = self.dec_to_hourformat((self.curr_len/self.day_len)*12)

        return temp_hour

    def night_relativeHour(self):
        """
        calculate the relative hour for the night    

        current_time = get datetime obj

        """
        self.night_len = abs(self.nd_sunrise - self.sunset)
        self.curr_len = abs(self.current_time - self.sunset)

        self.night_hour_len = (self.night_len/12/60).total_seconds()
        self.night_second_len = (self.night_hour_len/60)

        temp_hour = self.dec_to_hourformat((self.curr_len/self.night_len)*12)

        return temp_hour

    def lateNight_relativeHour(self):

        self.night_len = abs(self.sunrise - self.yt_sunset)
        self.curr_len = abs(self.current_time - self.yt_sunset)

        self.night_hour_len = (self.night_len/12/60).total_seconds()
        self.night_second_len = (self.night_hour_len/60)

        temp_hour = self.dec_to_hourformat((self.curr_len/self.night_len)*12)

        return temp_hour

    def now(self):

        super().__init__()

        if (self.current_time > self.sunset):
            temp_hour = self.night_relativeHour()
            self.dayORnight = "night"
            return temp_hour

        elif (self.current_time > self.sunrise) and (self.current_time < self.sunset):
            temp_hour = self.day_relativeHour()
            self.dayORnight = "day"
            return temp_hour

        elif self.current_time < self.sunrise:
            temp_hour = self.lateNight_relativeHour()
            self.dayORnight = "night"
            return temp_hour

        elif (self.current_time == self.sunrise) or (self.current_time == self.nd_sunrise):
            temp_hour = '00:00:00'
            self.dayORnight = "day"
            return temp_hour

        elif (self.current_time == self.sunset):
            temp_hour = '00:00:00'
            self.dayORnight = "night"
            return temp_hour

        else:
            raise ValueError('an error occored time doesnt have a slot')

    def reltive_to_standard(self, city, relative_time=None,day_night=None, date=None):
        '''
        - city in the string format ```"קרית שמונה"```
        - day_night = ```"day"``` or ```"night"``` depend on the state of the relative hour 
        - relative_time = ```"H:M:S"``` string format for relative time
        - date = ```"Y-m-d"``` string format for the date desired
        '''
        super().__init__()

        day_night = self.dayORnight if day_night is None else day_night
        date = datetime.now().date().isoformat() if date is None else date
        relative_time = self.now() if relative_time is None else relative_time

        lat, lon = get_coords(city)
        sun = Sun(lat, lon)

        dummy_date = datetime.strptime(f'{date} {"12:00:00"}', "%Y-%m-%d %H:%M:%S")

        sunrise = (sun.get_sunrise_time(date=dummy_date) +timedelta(hours=watch.utc_israel())).replace(tzinfo=None)
        sunset = (sun.get_sunset_time(date=dummy_date) +timedelta(hours=watch.utc_israel())).replace(tzinfo=None)
        yt_sunset = (sun.get_sunset_time(date=dummy_date+timedelta(days=-1))+timedelta(hours=watch.utc_israel())).replace(tzinfo=None)
        nd_sunrise = (sun.get_sunrise_time(date=dummy_date+timedelta(days=1))+timedelta(hours=watch.utc_israel())).replace(tzinfo=None)

        if day_night == "day":
            h, m ,s= relative_time.split(":")
            relative_sec = int(h)+(int(m)/60) +int(s)/3600
            
            day_sec = (sunset - sunrise)/12
            standard_hour = sunrise + day_sec*relative_sec
        
            return standard_hour

        elif day_night == "night":
            
            h, m ,s= relative_time.split(":")
            relative_sec = int(h)+(int(m)/60) + int(s)/3600
            
            night_sec = (nd_sunrise - sunset)/12
            standard_hour = sunset + night_sec*relative_sec

            return standard_hour

    def hebrew_date(self,date_str = None):
        '''
        date_str should be a string in this format "%Y-%m-%d"
        '''
        super().__init__()

        date_str = self.current_time.strftime("%Y-%m-%d") if date_str is None else date_str

        year_g, month_g, day_g = date_str.split('-')

        today_abs = self.gregorian_to_absdate(int(year_g), int(month_g), int(day_g))
        year_h, month_h, day_h = self.absdate_to_hebrew(today_abs)

        heb_date = self.hebrew_date_from_num(year_h, month_h, day_h)

        return heb_date
