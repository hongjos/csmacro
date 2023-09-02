"""
File: settings.py
Description: Just some globl variables used across scripts for now.
"""

def init():
    global dive_count
    global raid_count
    global game_pos

    dive_count = 0
    raid_count = 0
    game_pos = [-1, -1] # position of game icon in upper left corner
