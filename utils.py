import sys
import random
import pyautogui                                # mouse clicking
from python_imagesearch.imagesearch import *    # image detection

QUARTZ = 1
CONTRACT = 2

def rand_pause(num):
    """
    Add a small random number between 0 and 0.5.
    """
    return num + random.uniform(0, 0.5)

def goto_image(name, path):
    """
    Move mouse to some image.
    """
    # find image position
    pos = imagesearch(path)

    # move mouse
    if pos[0] != -1:
        pyautogui.moveTo(pos[0], pos[1])
    else:
        error_message = "Error: Can't find " + name + " image."
        sys.exit(error_message)
    
    return pos

def delay_click(x, y, delay, random=True):
    """
    Move mouse to (x,y) wait some time then click.
    """
    pyautogui.moveTo(x, y)

    if random:
        time.sleep(rand_pause(delay))
    else:
        time.sleep(delay)

    pyautogui.click()

def scroll_find(path):
    """
    Find position of an image. If not there, scroll down a bit and try again.
    """
    pos = imagesearch(path)

    # not found? scroll down
    if pos[0] == -1:
        for i in range(6):
            pyautogui.scroll(-10)
            time.sleep(rand_pause(0))
        pos = imagesearch(path)
    
    return pos