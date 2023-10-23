### date funcs


import datetime

def dt_x_minutes_ago(minutes, tzinfo=None):
    """Get datetime x minutes ago."""
    return datetime.datetime.now(tzinfo) - datetime.timedelta(minutes = minutes)
