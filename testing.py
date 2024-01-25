"""
File: testing.py
Description: For adhoc testing.
"""
from auto_utils import *

settings.init()
# initial game pos
init_game_pos()
print(f"Game Position:({settings.game_pos[0]}, {settings.game_pos[1]})")
text = image_to_text(region=(1433,482, 65, 20), is_number=True)
print(text)
# pyautogui.displayMousePosition()