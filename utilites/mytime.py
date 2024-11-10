from datetime import datetime, timedelta


def shoud_edit(message_date : datetime) -> bool:
    age = datetime.now() - message_date
    if age < timedelta(hours=48):
        return True 
    return False