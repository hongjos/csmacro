import sys
import random
import pyautogui                                # mouse clicking
from python_imagesearch.imagesearch import *    # image detection

QUARTZ = 1
CONTRACT = 2

def rand_pause(num, random=True):
    """
    Pause for some time + a small random amount (if random is true).
    """
    rand = random.uniform(0, 0.5) if random else 0
    time.sleep(num + rand)

def click_and_delay(x, y, delay=0, random=True):
    """
    Move mouse to (x,y) click then wait some time.
    """
    pyautogui.moveTo(x, y)
    rand_pause(delay, random)
    pyautogui.click()

def search_loop(path, delay=0.5, maxiter=10):
    """
    Search for image until found.
    """
    for i in range(maxiter):
        pos = imagesearch(path)
        # found image? break out of loop
        if pos[0] != -1:
            break
        time.sleep(delay)

    return pos 

def scroll_find(path):
    """
    Find position of an image. If not there, scroll down a bit and try again.
    """
    pos = imagesearch(path)

    # not found? scroll down
    if pos[0] == -1:
        for i in range(6):
            pyautogui.scroll(-10)
            rand_pause(0)
        pos = imagesearch(path)
    
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