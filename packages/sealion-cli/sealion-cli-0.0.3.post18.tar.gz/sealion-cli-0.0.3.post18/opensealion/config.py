import curses

'''sealion-cli version'''
version = "0.0.3.post18"

'''sealion-cli workspace path'''
sealion_cli_root = "$HOME/.sealion-cli"

'''logo and slogan'''
logos = [
    "=================================================================",
    "|   _____            _ _                    _____ _      _____  |",
    "|  / ____|          | (_)                  / ____| |    |_   _| |",
    "| | (___   ___  __ _| |_  ___  _ __ ______| |    | |      | |   |",
    "|  \___ \ / _ \/ _` | | |/ _ \| '_ \______| |    | |      | |   |",
    "|  ____) |  __/ (_| | | | (_) | | | |     | |____| |____ _| |_  |",
    "| |_____/ \___|\__,_|_|_|\___/|_| |_|      \_____|______|_____| |",
    f"|                                                  {version} |",
    "================================================================="
]
introduction = 'Start to create your own project with the Sealion-CLI.'

'''
goodbye page setting（display duration and content）
'''
goodbye_show_seconds = 3
goodbyes = [
    "Thank you for using Sealion-CLI             ",
    "Find more in https://github.com/open-sealion",
    "Bye-Bye~                                    ",
    f"Closing in {goodbye_show_seconds} seconds...                     ",
]

'''
menus
'''
menu_items = [
    "frontend",
    "backend ",
    "setting ",
    "exit    "
]
frontend = [
    "mm-template     ",
    "mm-template-vite",
    "mm-lib-template ",
    "back            "
]
backend = [
    "sealion-boot",
    "back        "
]
install = [
    "mvn          ",
    "nvm          ",
    "node         ",
    "conda        ",
    "back         "
]
setting = [
    "theme  ",
    "install",
    "network",
    "back   ",
]

previous_menu_map_dict = {
    "frontend": None,
    "backend": None,
    "setting": None,
    "mm-template": menu_items,
    "mm-template-vite": menu_items,
    "mm-lib-template": menu_items,
    "sealion-boot": menu_items,
    "theme": menu_items,
    "network": menu_items,
    "install": menu_items,
    "mvn": setting,
    "nvm": setting,
    "node": setting,
    "conda": setting,
    "green": setting,
    "red": setting,
    "cyan": setting,
    "magenta": setting,
    "white": setting,
    "black": setting,
}

theme_types = [
    {
        "f": curses.COLOR_GREEN,
        "b": curses.COLOR_BLACK
    },
    {
        "f": curses.COLOR_RED,
        "b": curses.COLOR_BLACK
    },
    {
        "f": curses.COLOR_BLACK,
        "b": curses.COLOR_WHITE
    },
    {
        "f": curses.COLOR_CYAN,
        "b": curses.COLOR_BLACK
    },
    {
        "f": curses.COLOR_MAGENTA,
        "b": curses.COLOR_BLACK
    },
    {
        "f": curses.COLOR_WHITE,
        "b": curses.COLOR_BLACK
    },
]
theme = [
    "green  ",
    "red    ",
    "black  ",
    "cyan   ",
    "magenta",
    "white  ",
    "back   ",
]

'''maven setting'''
maven_url = "https://dlcdn.apache.org/maven/maven-3/3.9.5/binaries/apache-maven-3.9.5-bin.tar.gz"
mvn_setting_url = 'https://oss.openmmlab.com/mvn_setting.xml'
mvn_setting_path = sealion_cli_root + '/mvn_setting.xml'

'''conda setting'''
conda_install_sh = "Miniconda3-latest-Linux-x86_64.sh"
conda_url = f"https://repo.anaconda.com/miniconda/{conda_install_sh}"
