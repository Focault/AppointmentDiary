
from UI import choose_room

ROOMS = (101, 102, 103, 404, 505)


def load_rooms():
    rooms = {}
    for room in ROOMS:
        rooms[room] = []
    return rooms


def list_available_room(_rooms_d, _start_t, _end_t):
    available = []
    for room, occupy_at in _rooms_d.items():
        for at in occupy_at:
            if _end_t <= at[0] or _start_t >= at[1]:
                continue
            else:
                break
        else:
            available.append(room)
    return available


def choose_available_room(_rooms_d, _start_t, _end_t):
    available = list_available_room(_rooms_d, _start_t, _end_t)
    return choose_room(available)


def update_room(_room_n, _room_d, _start_t, _end_t, _mode):
    if _mode:
        _room_d[_room_n].append((_start_t, _end_t))
    else:
        _room_d[_room_n].remove((_start_t, _end_t))
