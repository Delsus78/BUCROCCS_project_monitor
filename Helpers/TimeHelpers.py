import time


def get_actual_hour():
    """
    get the hour only of the day (in 24h format)
    :return: ex. 12 or 01 as integer
    """
    return time.strftime("%H")


def get_actual_day():
    """
    get the day of the week
    :return: ex. Monday or Friday
    """
    return time.strftime("%A")


def get_actual_day_from_int(i):
    """
    get the day of the week
    :return: ex. 'Monday' for 0 or 'Friday' for 4
    """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[i]


def get_actual_day_as_int():
    """
    get the day of the week
    :return: ex. 0 for Monday or 4 for Friday
    """
    return int(time.strftime("%w"))
