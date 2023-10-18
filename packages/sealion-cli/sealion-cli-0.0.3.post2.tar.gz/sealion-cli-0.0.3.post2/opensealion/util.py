import config


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
