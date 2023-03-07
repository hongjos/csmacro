from imports import *

class Branch:
    def __init__(self, name, pos, out_pos, default=False):
        self.name = name
        self.pos = pos
        self.default=default
        self.out_pos = out_pos # where to click to complete dispatch

        self.mission_type = 0
    
    def start_dispatch(self):
        # click on branch
        click_and_delay(self.pos[0], self.pos[1], delay=0.2, random=False)

        # check if still ongoing mission
        if self.still_ongoing():
           rand_pause(0.3) 
           return 
        
        # choose mission
        self.choose_mission()

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
        click_and_delay(self.pos[0], self.pos[1], 0.2, random=False)

        # check if still ongoing mission
        if self.still_ongoing():
           rand_pause(0.3) 
           return

        # click out of rewards
        pyautogui.moveTo(self.out_pos[0], self.out_pos[1])
        pyautogui.click(clicks=15, interval=0.3)
        time.sleep(1)

    def choose_mission(self):
        """
        Choose mission with priority (high to low): blue tix, 60 quartz, 1 hr.
        """
        # move to default mission
        p = search_loop("images/dispatch/replace.PNG")
        pyautogui.moveTo(p[0]+290, p[1]-280)
        rand_pause(0.1)
        # pyautogui.moveTo(1236, 661)

        # employee contract mission found?
        p = imagesearch("images/dispatch/contract.PNG")
        if p[0] != -1:
            click_and_delay(p[0], p[1]-50, delay=0)
            self.mission_type = CONTRACT
            return
        # quartz mission found?
        p = imagesearch("images/dispatch/quartz.PNG")
        if p[0] != -1:
            click_and_delay(p[0], p[1]-50, delay=0)
            self.mission_type = QUARTZ
            return
        # click default
        pyautogui.click()

    def still_ongoing(self):
        """
        Check if dispatch is still ongoing.
        """    
        p = imagesearch("images/dispatch/ongoing.PNG")
        
        # if still ongoing, return
        if p[0] != -1:
            p = search_loop("images/dispatch/return.PNG")
            click_and_delay(p[0], p[1], delay=0)
            return True
        else:
            return False
            

      