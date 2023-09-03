"""
File: game_auto.py
Description: Contains functions for going to each game state.
"""

from imports import *
from branch import Branch

def run_game(wait=60):
    """
    Start the game and go to home screen.
    ---
    wait : buffer time (in seconds)
    """
    # click game icon
    pos = search_loop("images/startup/icon.PNG", maxiter=30)
    pyautogui.doubleClick(pos[0]+5, pos[1]+5)
    rand_pause(3, False)

    # click start game and wait
    pos = search_loop("images/startup/game.PNG")
    rand_pause(wait)

    # check for update
    update = imagesearch("images/misc/confirm.PNG")
    # wait for game to update if there is one
    if found_position(update):
        pyautogui.click(update[0], update[1])
        time.sleep(200)
        # click into start game
        pyautogui.click(pos[0]+600, pos[1]+400)
        time.sleep(10)
    
    # click into home screen
    pyautogui.doubleClick(pos[0]+600, pos[1]+400)
    rand_pause(2)

    # exit out of game news pop up
    pos = search_loop("images/startup/x.PNG") 
    click_and_delay(pos[0]+5, pos[1]+5, delay=.5, rand=False)

    return pos

def exit_game(default=False):
    if default:
        click_and_delay(1719, 444, .01) # exit button
    else:
        pos = search_loop("images/misc/exit.PNG", maxiter=20)
        pyautogui.click(pos[0]+2, pos[1]+2)

#####################################################################
# Go to specific screens functions.
#####################################################################
def goto_world_map():
    """
    Go to the World Map from Home screen.
    """
    pos = search_loop("images/startup/world_map.PNG")
    pyautogui.click(pos[0], pos[1], clicks=3, interval=.3)
    rand_pause(2)

    return pos

def goto_explore_status():
    """
    Go to the Exploration Status from World Map.
    """
    

