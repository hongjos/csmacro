import sys
import random
import time
import datetime
import pyautogui                                # mouse clicking
from python_imagesearch.imagesearch import *    # image detection

QUARTZ = 1
CONTRACT = 2

def rand_pause(num, rand=True):
    """
    Pause for some time + a small random amount (if random is true).
    """
    add = random.uniform(0, 0.5) if rand else 0
    time.sleep(num + add)

def click_and_delay(x, y, delay=0, rand=True):
    """
    Move mouse to (x,y) click then wait some time.
    """
    pyautogui.moveTo(x, y)
    pyautogui.click()
    rand_pause(delay, rand)

def search_loop(path, delay=0.5, maxiter=10):
    """
    Search for image until found.
    """
    for i in range(maxiter):
        pos = imagesearch(path, precision=0.7)
        # found image? break out of loop
        if pos[0] != -1:
            break
        time.sleep(delay)

    return pos 

def scroll_find(path):
    """
    Find position of an image. If not there, scroll down a bit and try again.
    """
    pos = search_loop(path, delay=0.2, maxiter=2)

    # not found? scroll down
    if pos[0] == -1:
        for i in range(6):
            pyautogui.scroll(-10)
            rand_pause(0)
        pos = search_loop(path, delay=0.2, maxiter=2)
    
    return pos

def minimize_windows(maxiter=10):
    """
    Minimize any current windows on the screen.
    """
    # there shouldn't be too many windows on the screen
    for i in range(maxiter):
        pos = search_loop("images/misc/minimize.PNG", maxiter=2)
        if pos[0] != -1:
            click_and_delay(pos[0], pos[1], delay=.3)
        else:
            return