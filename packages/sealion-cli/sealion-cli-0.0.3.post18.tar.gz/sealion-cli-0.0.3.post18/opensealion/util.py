from subprocess import Popen, PIPE, STDOUT
import os
import curses
import config


height, width = 0, 0
COLOR_TYPE = 1


def get_main_menu(current_row: int) -> list:
    if current_row == 0:
        return config.frontend
    elif current_row == 1:
        return config.backend
    elif current_row == 2:
        return config.setting


def create_menu_dict(*menu_lists) -> dict:
    menu_dict = dict()
    for menu_list in menu_lists:
        for item in menu_list:
            # 去除字符串中的空格
            item = item.strip()
            menu_dict[item] = menu_list
    return menu_dict


def exe_shell(command: str, shell: str = '/bin/bash'):
    return Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, executable=shell)


def get_current_path():
    return os.getcwd()


def do_move_key(key, current_row, sub_items):
    if key == curses.KEY_UP:
        if current_row > 0:
            current_row -= 1
        else:
            current_row = len(sub_items) - 1
    elif key == curses.KEY_DOWN:
        if current_row < len(sub_items) - 1:
            current_row += 1
        else:
            current_row = 0
    return current_row


def is_move_key(key):
    return key == curses.KEY_UP or key == curses.KEY_DOWN


def is_ctrl_c(key):
    return key == -1

def is_enter_key(sub_key):
    return sub_key in [curses.KEY_ENTER, ord("\n")]


def is_back(menu: str):
    return "back" == menu.replace(" ", "")


def is_exit(menu: str):
    return "exit" == menu.replace(" ", "")


def get_parent_menu(current_menu):
    return config.previous_menu_map_dict.get(current_menu)


def debugger(stdscr, y: int = 0, x: int = 0, debug: str = ""):
    stdscr.addstr(y, x, debug)
    stdscr.getch()


def press_anykey_exit(stdscr):
    stdscr.attron(curses.color_pair(COLOR_TYPE))
    to_quit = "press any key to quit"
    stdscr.addstr(
        max(height - 1, 0), width // 2 - len(to_quit) // 2,
        to_quit,
        curses.color_pair(COLOR_TYPE) | curses.A_BLINK
    )
    stdscr.attroff(curses.color_pair(COLOR_TYPE))
    stdscr.getch()


def exe_shell_curses(command: str, stdscr, skip_press_anykey: bool = False):
    stdscr.clear()
    command = "echo 'START running shell script...' && " + command
    process = exe_shell(command, shell="/bin/bash")
    try:
        with (process.stdout):
            y = 0
            for line in iter(process.stdout.readline, b''):
                # s = str(line).replace("b'", "").replace("'", "").replace("\\n", "")
                s = line.decode('utf-8')
                stdscr.addstr(y, 0, s)
                stdscr.refresh()
                y += 1
                if y >= height - 1:
                    stdscr.clear()
                    y = 0
        if not skip_press_anykey:
            press_anykey_exit(stdscr)
    except Exception as e:
        stdscr.addstr(0, 0, f"error={e}")
        press_anykey_exit(stdscr)


def set_theme(color_type: int):
    global COLOR_TYPE
    COLOR_TYPE = color_type


def get_theme():
    return COLOR_TYPE


def init(h: int, w: int):
    global height, width
    height = h
    width = w
