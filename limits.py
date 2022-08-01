
DAY_START = 9.0
DAY_END = 18.0
MIN_APPOINTMENT = 0.25
MAX_APPOINTMENTS = int((DAY_END - DAY_START) // MIN_APPOINTMENT)


def check_time_legality(_start_t, _end_t):
    if DAY_START <= _start_t < _end_t <= DAY_END and (_end_t - _start_t) >= MIN_APPOINTMENT:
        return True
    return False
