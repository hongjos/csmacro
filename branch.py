from imports import *

class Branch:
    def __init__(self, name, pos, out_pos, default=False):
        self.name = name
        self.pos = pos
        self.default=default
        self.out_pos = out_pos # where to click to complete dispatch

        self.mission_type = 0
        self.in_progress = False
    
    def start_dispatch(self, last=False):
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
        self.choose_mission(last)

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
            p = search_loop("images/dispatch/return.PNG") # go back
            click_and_delay(p[0], p[1], delay=0.1)
            self.start_dispatch() # do mission
            self.in_progress = True
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

    def choose_mission(self, last=False):
        """
        Choose mission with priority (high to low): blue tix, 60 quartz, 1 hr.
        """
        # move to default (1 hr.) mission
        p = search_loop("images/dispatch/replace.PNG")
        pyautogui.moveTo(p[0]+290, p[1]-280)
        rand_pause(0.1)
        # pyautogui.moveTo(1236, 661)

        # employee contract mission found?
        p = imagesearch("images/dispatch/contract.PNG")
        if found_position(p):
            click_and_delay(p[0], p[1]-50, delay=0)
            self.mission_type = CONTRACT
            return
        # quartz mission found?
        p = imagesearch("images/dispatch/quartz2.PNG", precision=0.95)
        if found_position(p):
            click_and_delay(p[0], p[1]-50, delay=0)
            self.mission_type = QUARTZ
            return
        
        # click default mission
        if last:
            # move to 8 hr. mission
            pyautogui.click()
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
            