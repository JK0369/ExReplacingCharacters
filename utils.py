import datetime

# time
def get_ymd_time(milliseconds: int) -> datetime:
    time = datetime.datetime.fromtimestamp(milliseconds / 1000)
    return formatted_ymd_time(time)

def formatted_ymd_time(time: datetime) -> datetime:
    return time.strftime('%Y-%m-%d %H:%M:%S')

def get_is_over_time_from_now(target_minute: int) -> bool:
    current_time = datetime.datetime.now()
    one_hour_later = current_time + datetime.timedelta(minutes=target_minute)
    return one_hour_later < current_time

# variable
def get_variable_ratio(lhs: float, rhs: float) -> float:
    return abs(lhs - rhs) / max(lhs, rhs) * 100