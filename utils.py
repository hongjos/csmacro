"""
File: utils.py
Description: Some utilities for game auto.
"""

import sys
import os
import random
import time
import datetime
import csv
import smtplib, ssl
import pyautogui                                # mouse clicking
from python_imagesearch.imagesearch import *    # image detection

QUARTZ = 1
CONTRACT = 2
SIM = 3

def found_position(pos):
    """
    Returns true if the position given is found (not -1).
    """
    if pos[0] != -1:
        return True
    else:
        return False
    
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

def search_loop(path, delay=0.5, maxiter=10, accuracy=0.7):
    """
    Search for image until found.
    """
    for i in range(maxiter):
        pos = imagesearch(path, precision=accuracy)
        # found image? break out of loop
        if found_position(pos):
            break
        time.sleep(delay)

    return pos 

def minimize_windows(maxiter=5):
    """
    Minimize any current windows on the screen.
    """
    # there shouldn't be too many windows on the screen
    for i in range(maxiter):
        pos = search_loop("images/misc/minimize2.PNG", maxiter=2)         # cmd prompt

        # if not found_position(pos):
            # pos = search_loop("images/misc/minimize.PNG", maxiter=2)    # vs code  

        if found_position(pos):
            click_and_delay(pos[0], pos[1], delay=.3)
        else:
            return

def no_internet():
    """
    Returns true if there is no internet connection.
    """
    pos = imagesearch("images/misc/no_internet.PNG")
    if found_position(pos):
        print("No internet connection.")
        return True
    return False

def send_mail(text, email="waterabottle@gmail.com"):
    """
    Send some text to an email.
    """
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "waterabottle@gmail.com"  
    receiver_email = email
    password = "dpjklrcricpjjlzt"

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
    except Exception:
        print("Email failed to send.")
        pass

def get_var(var_name, file_name="var.txt"):
    """
    Get the value of a variable from the var.txt file.
    """
    var_name = var_name.lower()
    with open(file_name, 'r') as f:
        for line in f:
            name, val = line.strip().split('=')
            if name == var_name:
                return val
    return None

def set_var(var_name, new_val, file_name="var.txt"):
    """
    Set the value of a variable from the var.txt file.
    """
    var_name = var_name.lower()
    with open(file_name, 'r') as f:
        lines = f.readlines()

    with open(file_name, 'w') as f:
        for line in lines:
            name, _ = line.strip().split('=')
            if name == var_name:
                f.write(f'{name}={new_val}\n')
            else:
                f.write(line)
    
def shut_down():
    """
    Shut down the computer.
    """
    os.system('shutdown -s -t 0')
