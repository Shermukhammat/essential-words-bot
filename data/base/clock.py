from datetime import datetime
import pytz


time_in_tashkent = pytz.timezone("Asia/Tashkent")

def now() -> str:
    now = datetime.now(time_in_tashkent)
    return f"{now.year}.{now.month}.{now.day} {now.hour}:{now.minute}"