import sys
import random
import time
import datetime
import smtplib, ssl
import pyautogui                                # mouse clicking
from python_imagesearch.imagesearch import *    # image detection

QUARTZ = 1
CONTRACT = 2

def found_position(pos):
    """
    Returns true if found position.
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
        if pos[0] != -1:
            break
        time.sleep(delay)

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

def no_internet():
    """
    Returns true if there is no internet connection.
    """
    pos = imagesearch("images/misc/no_internet.PNG")
    if pos[0] != -1:
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