"""
File: game_auto.py
Description:
"""

from auto_utils import *

def main():
    pyautogui.FAILSAFE = False # move mouse to upper left to abort
    settings.init() # initialize global variables

    get_game_pos()

    

if __name__ == "__main__":
    main()