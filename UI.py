
import shutil
from participants import PARTICIPANTS
from limits import DAY_START, DAY_END, MIN_APPOINTMENT, check_time_legality


def choose_participants():
    invite = set()
    print("\nPotential Participants:")
    for idx, participant in enumerate(PARTICIPANTS):
        print((idx + 1), ": ", participant, end='\n', sep='')
    print("\nWhen Finished Enter 'q'\n")
    while True:
        try:
            who = input("Choose Participant For Meeting: ")
            if who.isalpha() and who.lower() == 'q':
                if not invite:
                    print("Meetings must have at least one participant.")
                    continue
                break
            who = PARTICIPANTS[int(who) - 1]
            if who in invite:
                invite.remove(who)
                print(who, "Removed From Meeting")
                continue
            invite.add(who)
            print(who, "Added To Meeting")
        except (ValueError, TypeError):
            print("Please Enter Only Number in range or 'q'")
        except IndexError:
            print("Out of Range.")
    return tuple(invite)


def choose_room(_rooms):
    if _rooms:
        print("\nAvailable Rooms:")
        for x in _rooms:
            print("Room", x)
        while True:
            try:
                room = int(input("\nChoose Room: "))
                if room in _rooms:
                    return room
                print("Please Enter Only Valid Room Number")
            except (ValueError, TypeError):
                print("Please Enter Only Valid Room Number")
    else:
        print("No Room Is Available At The Time You Chose. Try Choosing Another Time.")
        return False


def ask_for_time():
    while True:
        try:
            start_time = float(input("\nPlease Enter Start Time (in float format): "))
            end_time = float(input("Please Enter End Time (in float format): "))
            if not check_time_legality(start_time, end_time):
                print("Illegal Time For Meeting. Meetings should be at least", MIN_APPOINTMENT,
                      "long, and must be between", DAY_START, "and", DAY_END)
                continue
            return start_time, end_time
        except (ValueError, TypeError):
            print("Please Enter Only Valid Room Number")


def accept_alternative(_found, _start_t, _end_t, _room):
    time_period = "{0:}-{1:}"
    print("\n\nUnfortunately, not all the participants are available at the time you chose", end='')
    if _found:
        print(".\nThe meeting can be rescheduled to", time_period.format(_start_t, _end_t), "at room", _room)
        while True:
            try:
                accept = input("\nAccept Alternative? (y/n) ")
                if accept.lower() == 'y':
                    return True
                if accept.lower() == 'n':
                    return False
                raise ValueError
            except (ValueError, TypeError):
                print("Wrong Input.")
    else:
        print(",\nor at any other time today.")
    return False


def print_diary(_date, _meetings):
    if _meetings:
        width = shutil.get_terminal_size((80, 20))[0]
        header = "Appointment Diary For " + _date
        print("\n", header.center(width), sep='', end=' ')
        meeting_f = "\n\nMeeting No. {0:^3}\nStarts At: {1:^4}\t\t\tEnds At: {2:^4}\nAt Room No. {3:^3}\nParticipants:"
        for idx, meet in enumerate(_meetings):
            print(meeting_f.format(idx + 1, meet[0], meet[1], meet[2]), end=' ')
            print(*meet[3], sep=', ')
    else:
        print("\nAppointment Diary is Empty")


def print_status(_task, _status):
    prompt = " Finished Successfully!" if _status else " Failed."
    print("\n", _task, prompt, sep='')


def ask_option(_menu):
    width = shutil.get_terminal_size((80, 20))[0]
    print("", "Main Menu      ".center(width), sep="\n", end="\n\n")
    option_f = "For {0:^30} Type {1:^5}"
    for idx, item in enumerate(_menu):
        print(option_f.format(item[0], item[1]).center(width))
    while True:
        try:
            option = int(input("\nInsert Option: "))
            if option < 0 or option >= len(_menu):
                raise ValueError
            return option
        except (ValueError, TypeError):
            print("Please Insert Valid Option.\n\n")


def chose_appointment(_meetings_n):
    while True:
        try:
            meeting = int(input("\nPlease Choose Meeting No. : ")) - 1
            if 0 <= meeting < _meetings_n:
                return meeting
            raise ValueError
        except (ValueError, TypeError):
            print("Please Insert Valid Option.\n\n")


def ask_date():
    date_f = "{2:2}-{1:2}-{0:4}"
    while True:
        try:
            year = input("Please Insert Year (YYYY): ")
            if year.isnumeric() and len(year) == 4:
                month = input("Please Insert Month (MM): ")
                if month.isnumeric() and len(month) == 2:
                    day = input("Please Insert Day (DD): ")
                    if day.isnumeric() and len(day) == 2:
                        return date_f.format(year, month, day)
            raise ValueError
        except (ValueError, TypeError):
            print("Please Insert Valid Option. Adding Zeroes to Accommodate Length is Crucial.\n\n")


def search_by():
    print("\nSearch By:")
    print('\n'.join('{}: {}'.format(idx + 1, param)
                    for idx, param in enumerate(["Start Time", "End Time", "Room No.", "Participant"])))
    while True:
        try:
            search_p = int(input("\nPlease Choose Search Parameter: ")) - 1
            search_key = input("Search For: ")
            if 0 <= search_p <= 1:
                return search_p, float(search_key)
            if search_p == 2 and search_key.isnumeric():
                return search_p, int(search_key)
            if search_p == 3 and search_key.isalpha():
                return search_p, search_key
            raise ValueError
        except (ValueError, TypeError):
            print("Please Insert Valid Option.\n\n")
