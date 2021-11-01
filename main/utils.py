from datetime import datetime, timedelta

def get_future_date(days = 30):

    return datetime.now() + timedelta(days = days)