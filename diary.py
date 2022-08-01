
from datetime import date
from participants import load_participants, update_participants
from rooms import load_rooms, update_room
from UI import ask_date, ask_option, print_status, print_diary, chose_appointment, search_by
from meeting import process_appointment, create_meeting


def create_diary():
    diary_date = "-".join(str(date.today()).split("-")[::-1])
    participants = load_participants()
    rooms = load_rooms()
    diary = {"meetings": [],
             "date": diary_date,
             "participants": participants,
             "rooms": rooms}
    return diary


def save_diary(_diary):
    meeting_n = len(_diary["meetings"])
    if meeting_n:
        file_name_f = "{0}.Diary"
        meeting_f = "{0}\n{1}\n{2}\n"
        file = open(file_name_f.format(_diary["date"]), "w")
        for idx, meeting in enumerate(_diary["meetings"]):
            file.write(str(meeting_f.format(meeting[0], meeting[1], meeting[2])))
            print(*meeting[3], file=file, sep=', ')
            if idx != meeting_n - 1:
                file.write("\n")
        file.close()
        return True
    return False


def read_meeting(_file_o):
    return float(_file_o.readline()[:-1]), float(_file_o.readline()[:-1]), \
            int(_file_o.readline()[:-1]), tuple(_file_o.readline()[:-1].split(", "))


def load_diary(_old_diary):
    file_name = ask_date()
    try:
        file = open(file_name + ".Diary", "r")
        diary = create_diary()
        start_t, end_t, room_n, guests = read_meeting(file)
        result, meeting = process_appointment(diary["rooms"], diary["participants"], start_t, end_t, room_n, guests)
        if result:
            add_meeting(diary, meeting)
            while f := file.read(1):
                start_t, end_t, room_n, guests = read_meeting(file)
                result, meeting = \
                    process_appointment(diary["rooms"], diary["participants"], start_t, end_t, room_n, guests)
                if not result:
                    break
                add_meeting(diary, meeting)
            else:
                _old_diary["date"] = file_name
                _old_diary["rooms"] = diary["rooms"]
                _old_diary["participants"] = diary["participants"]
                _old_diary["meetings"] = diary["meetings"]
                return True
        return False
    except FileNotFoundError:
        print_status("File Not Found.", False)
        return False


def add_meeting(_diary, _meeting):
    _diary["meetings"].append(_meeting)
    _diary["meetings"].sort(key=lambda meeting: meeting[0])
    update_room(_meeting[2], _diary["rooms"], _meeting[0], _meeting[1], True)
    update_participants(_meeting[3], _diary["participants"], _meeting[0], _meeting[1], True)


def create_appointment(_diary):
    result, meeting = create_meeting(_diary["rooms"], _diary["participants"])
    if result:
        add_meeting(_diary, meeting)
    print_status("Creating Appointment", result)


def search_appointment(_diary):
    status, result = "", False
    if _diary["meetings"]:
        param, key = search_by()
        meetings = []
        if param != 3:
            for meet in _diary["meetings"]:
                if meet[param] == key:
                    meetings.append(meet)
        else:
            for meet in _diary["meetings"]:
                if key in meet[param]:
                    meetings.append(meet)
        if meetings:
            print_diary("'" + str(key) + "'" + " Search Results", meetings)
            status, result = "Searching Appointment", True
        else:
            status = "No Results Found For " + "'" + str(key) + "'."
    else:
        status = "Diary is Empty."
    print_status(status, result)


def delete_appointment(_diary):
    print_diary(_diary["date"], _diary["meetings"])
    result = False
    if _diary["meetings"]:
        meeting = _diary["meetings"].pop(chose_appointment(len(_diary["meetings"])))
        update_room(meeting[2], _diary["rooms"], meeting[0], meeting[1], False)
        update_participants(meeting[3], _diary["participants"], meeting[0], meeting[1], False)
        result = True
    print_status("Deleting Appointment", result)


def save_diary_m(_diary):
    print_status("Saving Diary", save_diary(_diary))


def load_diary_m(_diary):
    print_status("Loading Diary", load_diary(_diary))


def print_diary_m(_diary):
    print_diary(_diary["date"], _diary["meetings"])


MENU = (("Create Appointment", 1, create_appointment),
        ("Search Appointment", 2, search_appointment),
        ("Delete Appointment", 3, delete_appointment),
        ("Save Diary", 4, save_diary_m),
        ("Load Diary", 5, load_diary_m),
        ("Print Diary", 6, print_diary_m),
        ("Exit", 0))


def manage_diary():
    diary = create_diary()
    option = ask_option(MENU)
    while option:
        MENU[option - 1][2](diary)
        option = ask_option(MENU)
