from imports import *

class Branch:
    def __init__(self, name, pos, out_pos, default=False):
        self.name = name
        self.pos = pos
        self.default=default
        self.out_pos = out_pos # where to click to complete dispatch

        self.mission_type = 0
        self.raid_in_progress = False
    
    def start_dispatch(self):
        # click on branch
        delay_click(self.pos[0], self.pos[1], 0.2, random=False)

        # check if still ongoing mission
        if self.still_ongoing():
           time.sleep(rand_pause(0.3)) 
           return 
        
        # choose mission
        self.choose_mission()

        # do mission
        if self.default:
            delay_click(1334, 855, delay=0.01)  # click ok
            delay_click(833, 483, delay=0.01)   # return
        else:
            p = goto_image("ok", "images/dispatch/ok.PNG")
            delay_click(p[0], p[1], delay=0.1)

            p = goto_image("return", "images/dispatch/return.PNG")
            delay_click(p[0], p[1], delay=0.1)

        time.sleep(rand_pause(0.3))
    
    def complete_mission(self):
        # click on branch
        self.mission_type = 0
        delay_click(self.pos[0], self.pos[1], 0.2, random=False)

        # check if still ongoing mission
        if self.still_ongoing():
           time.sleep(rand_pause(0.3)) 
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
        p = goto_image("replace", "images/dispatch/replace.PNG")
        pyautogui.move(290, -280)
        # pyautogui.moveTo(1236, 661)

        # blue tix mission?
        p = imagesearch("images/dispatch/contract.PNG")
        if p[0] != -1:
            delay_click(p[0], p[1]-50, delay=0.1)
            self.mission_type = CONTRACT
            return
        # quartz mission?
        p = imagesearch("images/dispatch/quartz.PNG")
        if p[0] != -1:
            delay_click(p[0], p[1]-50, delay=0.1)
            self.mission_type = QUARTZ
            return
        # click default
        time.sleep(rand_pause(0.1))
        pyautogui.click()

    def still_ongoing(self):
        """
        Check if dispatch is still ongoing.
        """    
        p = imagesearch("images/dispatch/ongoing.PNG")
        if p[0] != -1:
            p = goto_image("return", "images/dispatch/return.PNG")
            delay_click(p[0], p[1], delay=0.1)
            return True
        else:
            return False
            

      