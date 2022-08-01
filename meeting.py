
from UI import choose_participants, ask_for_time, accept_alternative
from rooms import choose_available_room, list_available_room
from participants import check_on_guests
from limits import check_time_legality, MAX_APPOINTMENTS, MIN_APPOINTMENT


def suggest_alternative(_invite, _rooms_d, _participants_d, _start_t, _end_t, _room):
    for level in range(1, MAX_APPOINTMENTS):
        flag = 0
        for factor in [level * MIN_APPOINTMENT, level * MIN_APPOINTMENT * -1]:
            if check_time_legality(_start_t + factor, _end_t + factor):
                rooms_available = list_available_room(_rooms_d, _start_t + factor, _end_t + factor)
                if rooms_available:
                    if check_on_guests(_invite, _participants_d, _start_t + factor, _end_t + factor):
                        room = _room if _room in rooms_available else rooms_available[0]
                        return True, _start_t + factor, _end_t + factor, room
            else:
                flag += 1
        if flag == 2:
            break
    return False, _start_t, _end_t, _room


def create_meeting(_rooms_d, _participants_d):
    invite = ()
    while True:
        start_time, end_time = ask_for_time()
        room = choose_available_room(_rooms_d, start_time, end_time)
        if not room:
            continue
        invite = choose_participants()
        if check_on_guests(invite, _participants_d, start_time, end_time):
            break
        else:
            found, start_time, end_time, room = \
                suggest_alternative(invite, _rooms_d, _participants_d, start_time, end_time, room)
            if accept_alternative(found, start_time, end_time, room):
                break
            return False, ()
    return True, (start_time, end_time, room, invite)


def process_appointment(_rooms_d, _participants_d, _start_t, _end_t, _room_n, _guests):
    if check_time_legality(_start_t, _end_t) and \
        _room_n in list_available_room(_rooms_d, _start_t, _end_t) and \
            check_on_guests(_guests, _participants_d, _start_t, _end_t):
        return True, (_start_t, _end_t, _room_n, _guests)
    return False, ()
