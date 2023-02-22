import time
from os import system, name


def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def three_two_one_timer():
    print("3 ...")
    time.sleep(1)
    print("2 ...")
    time.sleep(0.75)
    print("1 ...")
    time.sleep(0.5)
