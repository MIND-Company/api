from .models import ParkingInfo, Price, Park, DayOfWeek
from datetime import datetime, timedelta, time
import pytz
import math


def calculate_price(parkingInfo: ParkingInfo):

    if parkingInfo.calculated_price:
        return parkingInfo.calculated_price

    timezone = pytz.timezone(parkingInfo.timezone)
    now_time = datetime.now(timezone)
    splited = split_by_day(parkingInfo.entry_time_utc, now_time, timezone)

    days_of_week = set([DayOfWeek.ALL, DayOfWeek.WEEKEND])
    for date in splited.keys():
        days_of_week.add(DayOfWeek.DAY_NUMBER_TO_DAY[date.weekday()])

    prices = Price.objects.filter(
        park=parkingInfo.park, day_of_week__in=days_of_week)
    day_to_price = {}
    for price in prices:
        day_to_price[price.day_of_week] = price

    calculated_prices = {}
    for date in splited.keys():
        day = DayOfWeek.DAY_NUMBER_TO_DAY[date.weekday()]
        price = day_to_price.get(day)
        if price is None and DayOfWeek.is_weekend(day):
            price = day_to_price.get(DayOfWeek.WEEKEND)
        if price is None:
            price = day_to_price.get(DayOfWeek.ALL)
        if price is None:
            raise ValueError("Price is undefined")

        calculated_prices[date] = calculate(splited[date], price)

    return sum(i for i in calculated_prices.values())


def calculate(time: timedelta, price: Price):

    minutes = math.ceil(time.seconds // 60)
    if price.free_time_in_minutes:
        minutes = max(minutes - price.free_time_in_minutes, 0)

    if minutes == 0:
        return round(0, 2)

    hours = math.ceil(minutes / 60)
    if price.max_price_per_day:
        return round(min(hours * price.price_per_hour, price.max_price_per_day), 2)

    return round(hours * price.price_per_hour, 2)


def split_by_day(begin_time: datetime, end_time: datetime, timezone) -> dict:

    begin_time = begin_time.astimezone(timezone)
    # end_time = end_time.astimezone(timezone) уже в нужном tz

    begin_date = begin_time.date()
    midnight = datetime.combine(
        begin_date, time(0, 0, 0, 0, timezone)) + timedelta(days=1)
    time_until_midnight = midnight - begin_time

    delta = end_time - begin_time
    if delta < time_until_midnight:
        return {begin_date: delta}

    result = {begin_date: time_until_midnight}
    delta -= time_until_midnight

    date = begin_date + timedelta(days=1)
    while delta > timedelta(hours=24):
        result[date] = timedelta(hours=24)
        date += time(days=1)
        delta -= timedelta(hours=24)

    result[date] = delta

    return result
