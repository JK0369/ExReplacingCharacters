import datetime

# time
def convert_unix_to_datetime(milliseconds: int) -> datetime:
    seconds_timestamp = milliseconds / 1000.0
    return datetime.datetime.utcfromtimestamp(seconds_timestamp)

def get_ymd_time(milliseconds: int) -> datetime:
    time = datetime.datetime.fromtimestamp(milliseconds / 1000)
    return formatted_ymd_time(time)

def formatted_ymd_time(time: datetime) -> datetime:
    return time.strftime('%Y-%m-%d %H:%M:%S')

def get_now_formatted_ymd_time() -> datetime:
    return formatted_ymd_time(datetime.datetime.now())

def get_is_over_time_from_now(target_minute: int) -> bool:
    current_time = datetime.datetime.now()
    later = current_time + datetime.timedelta(minutes=target_minute)
    return later < current_time

def get_is_over_3_days_from_now(milliseconds: int) -> bool:
    current_time = datetime.datetime.now()
    later = convert_unix_to_datetime(milliseconds) + datetime.timedelta(days=3)
    return later < current_time

# variable
def get_variable_ratio(lhs: float, rhs: float) -> float:
    return abs(lhs - rhs) / max(lhs, rhs) * 100