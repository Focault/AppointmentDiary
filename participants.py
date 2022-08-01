PARTICIPANTS = ("John",
                "Eric",
                "Terry",
                "Shahar",
                "Ron",
                "Roy",
                "Noa",
                "Michal",
                "Kyle",
                "Kenny",
                "Brian",
                "Luke")


def load_participants():
    participants = {}
    for name in PARTICIPANTS:
        participants[name] = []
    return participants


def check_on_guests(_invite, _participants_d, _start_t, _end_t):
    for guest in _invite:
        for meeting in _participants_d[guest]:
            if _end_t <= meeting[0] or _start_t >= meeting[1]:
                continue
            else:
                return False
    return True


def update_participants(_invite, _participants_d, _start_t, _end_t, _mode):
    for guest in _invite:
        if _mode:
            _participants_d[guest].append((_start_t, _end_t))
        else:
            _participants_d[guest].remove((_start_t, _end_t))
