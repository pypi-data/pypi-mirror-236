from django.utils import timezone


def round_to_nearest_hour(t: timezone.datetime):
    """
    Round a datetime object to the nearest hour.
    :param t: datetime.datetime object.
    :return: datetime.datetime object.
    """
    if not isinstance(t, timezone.datetime):
        raise TypeError("t must be a timezone.datetime object")

    return t.replace(
        minute=0, second=0, microsecond=0, hour=t.hour
    ) + timezone.timedelta(hours=(t.hour // 30))
