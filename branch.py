"""
File: branch.py
Description: Class for each of the branches. Each class contains their position
and methods to start a dispatch mission.
"""

from utils import *

class Branch:
    def __init__(self, name, pos, out_pos, default=False):
        self.name = name
        self.pos = pos
        self.default=default
        self.out_pos = out_pos # where to click to complete dispatch

        self.mission_type = 0
        self.in_progress = False
    
    def start_dispatch(self, mission_time=1):
        # if mission in progress, no need to do anything
        if self.in_progress:
            return
        
        # click on branch
        click_and_delay(self.pos[0], self.pos[1], delay=0.2, rand=False)

        # check if still ongoing mission
        if self.still_ongoing():
           rand_pause(0.3) 
           return 
        
        # choose mission
        self.choose_mission(mission_time)

        # do mission
        if self.default:
            click_and_delay(1334, 855, delay=0.01)  # click ok
            click_and_delay(833, 483, delay=0.01)   # return
        else:
            p = search_loop("images/dispatch/ok.PNG")       # start mission
            click_and_delay(p[0], p[1], delay=0.1)
            p = search_loop("images/dispatch/return.PNG")   # go back
            click_and_delay(p[0], p[1], delay=0.1)

        rand_pause(0.3)
    
    def complete_mission(self):
        # click on branch
        self.mission_type = 0
        click_and_delay(self.pos[0], self.pos[1], 0.2, rand=False)

        # check if branch isn't doing anything
        p = imagesearch("images/dispatch/replace.PNG")
        if found_position(p):
            # go back
            p = search_loop("images/dispatch/return.PNG") 
            click_and_delay(p[0], p[1], delay=0.1)
            # self.start_dispatch() # do mission
            # self.in_progress = True
            return

        # check if still ongoing mission
        if self.still_ongoing():
           rand_pause(0.3)
           self.in_progress = True 
           return

        # click out of rewards
        pyautogui.moveTo(self.out_pos[0], self.out_pos[1])
        pyautogui.click(clicks=15, interval=0.3)
        self.in_progress = False
        time.sleep(1)

    def choose_mission(self, mission_time=1):
        """
        Choose mission with priority (high to low): blue tix, simulation, quartz
        """
        # get default mission positions
        default_p = search_loop("images/dispatch/replace.PNG")
        rand_pause(0.1)

        # employee contract mission found?
        p = imagesearch("images/dispatch/contract.PNG")
        if found_position(p):
            click_and_delay(p[0], p[1]-50, delay=0)
            self.mission_type = CONTRACT
            return
        # simulation mission found?
        p = imagesearch("images/dispatch/sim.PNG")
        if found_position(p):
            # check if 4-hour mission
            if p[0] < default_p[0]+570:
                click_and_delay(p[0], p[1]-50, delay=0)
                self.mission_type = SIM
                return
        # quartz mission found?
        # p = imagesearch("images/dispatch/quartz.PNG")
        # if found_position(p):
        #     click_and_delay(p[0], p[1]-50, delay=0)
        #     self.mission_type = QUARTZ
        #     return
        
        # click on default mission
        if mission_time == 8:
            pyautogui.moveTo(default_p[0]+690, default_p[1]-280)
        elif mission_time == 4:
            pyautogui.moveTo(default_p[0]+490, default_p[1]-280)
        else:
            pyautogui.moveTo(default_p[0]+290, default_p[1]-280)
        pyautogui.click()

    def still_ongoing(self):
        """
        Check if dispatch is still ongoing.
        """    
        p = imagesearch("images/dispatch/ongoing.PNG", precision=0.85)
        
        # if still ongoing, return
        if found_position(p):
            p = search_loop("images/dispatch/return.PNG")
            click_and_delay(p[0], p[1], delay=0)
            return True
        else:
            return False
            