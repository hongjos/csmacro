"""
File: auto_utils.py
Description: Contains functions for going to each game state.
Some functions have a default parameter, setting it to true, doesn't use image search.
#TODO: Add default locations
"""

from utils import *
import settings
from branch import Branch

#####################################################################
# Game start up functions.
#####################################################################
def run_game(startup_buffer=60, default=False):
    """
    Start the game and go to home screen.
    """
    # click game icon
    if default: 
        pyautogui.doubleClick(110, 230)
    else:
        pos = search_loop("images/startup/icon.PNG", maxiter=30)
        pyautogui.doubleClick(pos[0]+5, pos[1]+5)
    rand_pause(3, False)

    # wiat for game to start
    pos = search_loop("images/startup/game.PNG")
    rand_pause(startup_buffer)

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

def exit_game():
    pos = search_loop("images/misc/exit.PNG", maxiter=20)
    pyautogui.click(pos[0]+2, pos[1]+2)

def init_game_pos(default=False):
    """
    Save the position of the game (upper left corner). 
    Need to initialize settings first.
    """
    if default:
        settings.game_pos = [817, 442]
    else:
        pos = imagesearch("images/misc/game.PNG")
        settings.game_pos = [pos[0], pos[1]]

#####################################################################
# Dispatch related functions.
#####################################################################
def goto_world_map():
    pos = search_loop("images/startup/world_map.PNG")
    pyautogui.click(pos[0], pos[1], clicks=3, interval=.3)
    rand_pause(2)

    return pos

def initialize_branches(default=True):
    """
    Save positions of each branch.
    """
    branches = []
    branch_names = ["ADC-G1", "Chamber", "Campamento", "Front Bay", "Lotus", "Charade"]
    images = ["adcg1", "chamber", "campamento", "frontbay", "lotus", "charade"]
    default_pos = [[398, 199], [703, 185], [900, 350], [410, 466], [46, 307], [204, 161]]
    
    # get outclick position
    out_pos = [settings.game_pos[0]+920, settings.game_pos[1]+203] 
    if not default:
        # find rightmost branch 
        pos = search_loop("images/branch/campamento.PNG")
        # store outclick position   
        out_pos = [pos[0]+70, pos[1]-195]                 

    # get/save positions of each branch
    for i, name in enumerate(branch_names):
        if default:
            pos_x = settings.game_pos[0] + default_pos[i][0]
            pos_y = settings.game_pos[1] + default_pos[i][1]
            position = [pos_x, pos_y]
            branches.append(Branch(name, position, out_pos))
        else:
            path = "images/branch/" + images[i] + ".PNG"
            pos = search_loop(path)
            # add branch if found
            if found_position(pos):
                pyautogui.moveTo(pos[0], pos[1])
                position = [pos[0]+10, pos[1]-30]
                branches.append(Branch(name, position, out_pos))
    
    return branches

def do_missions(branches: list[Branch], mission_time=1):
    for branch in branches:
        branch.start_dispatch(mission_time)

def complete_missions(branches: list[Branch]):
    for branch in branches:
        branch.complete_mission()

#####################################################################
# Dive/Raid related functions.
#####################################################################    
def complete_raids():
    # go to exploration status
    pos = search_loop("images/disturbance/explore.PNG")         
    click_and_delay(pos[0], pos[1], delay=0.5)
    # click raid history
    pos = search_loop("images/disturbance/raid_history.PNG")    
    click_and_delay(pos[0], pos[1], delay=0.5)
    # click complete all
    click_and_delay(pos[0]+710, pos[1]+211, delay=0)            
    pyautogui.moveTo(pos[0]+860, pos[1]-80)        
    pyautogui.click(clicks=5, interval=0.3)
    # exit exploration
    pos = search_loop("images/disturbance/explore_exit.PNG")
    click_and_delay(pos[0]+5, pos[1]+5, delay=0.5)  

def find_disturbances(do_raids=True, max_dives=5, sweep=False):
    """
    Search and complete for dives/raids until there are no more or limit reached.  
    """
    for i in range(6):
        # go to exploration status
        pos = search_loop("images/disturbance/explore.PNG")
        # check if exploration status found
        if not found_position(pos):
            print("Error: Cannnot find Exploration Status.")
            return
        click_and_delay(pos[0], pos[1], delay=0.5)

        # search for raids and send support requests
        pos = raid_support(do_raids)
        # if no raids, search for dives
        if not found_position(pos):
            if settings.dive_count >= max_dives:
                pos = [-1, -1]
            else:
                pos = complete_dive(sweep)

        # if no disturbances left, exit out
        if not found_position(pos):
            pos = search_loop("images/disturbance/explore_exit.PNG")
            click_and_delay(pos[0]+5, pos[1]+5, delay=0.5)              
            return            

def raid_support(do_raids):
    pos = search_loop("images/disturbance/raid.PNG", delay=0.2, maxiter=2, accuracy=0.85)

    if found_position(pos):
        if do_raids:
            # click go
            click_and_delay(pos[0]+570, pos[1]+40, delay=.5)
            # click support request
            pos = search_loop("images/disturbance/support_req.PNG")
            click_and_delay(pos[0], pos[1], delay=.5)
            # confirm request
            pos = search_loop("images/disturbance/raid_ok.PNG")
            click_and_delay(pos[0], pos[1], delay=.5)
            # go back
            pos = search_loop("images/dispatch/return.PNG")
            click_and_delay(pos[0], pos[1], delay=.5)
            # exit exploraion tab if needed
            pos_exit = search_loop("images/disturbance/explore_exit.PNG")
            if found_position(pos_exit):
                pos = pos_exit
                click_and_delay(pos[0]+5, pos[1]+5, delay=0.5)
        else:
            # click delete
            click_and_delay(pos[0]+570, pos[1], delay=.1)
            # confirm delete
            pos = search_loop("images/dispatch/ok.PNG")
            click_and_delay(pos[0], pos[1])
            # exit exploration tab
            pos = search_loop("images/disturbance/explore_exit.PNG")
            click_and_delay(pos[0], pos[1])           
        settings.raid_count += 1 
    
    return pos

def complete_dive(sweep):
    pos = search_loop("images/disturbance/dive.PNG", delay=0.2, maxiter=2)

    if found_position(pos):
        click_and_delay(pos[0]+580, pos[1]+10, delay=3)

        if sweep:
            pos = search_loop("images/disturbance/sweep.PNG")
            # only sweep if sweep button found
            if found_position(pos):
                click_and_delay(pos[0]+15, pos[1]+15, delay=.5, rand=False)
                # start dive
                pos = search_loop("images/disturbance/start_dive.PNG")
            if not found_position(pos):
                # this shouldn't happen but exit game just in case
                exit_game()
                return
            # click and wait for dive to finish
            click_and_delay(pos[0], pos[1], delay=150)
        else:
            pos = search_loop("images/disturbance/start_dive.PNG")
            # click and wait for dive to finish
            click_and_delay(pos[0], pos[1], delay=450)

        # make sure dive is finished
        pos = search_loop("images/disturbance/explore.PNG", delay=15, maxiter=60)
        if not found_position(pos):
            print("Error: Dive Incomplete")
            exit_game()

        settings.dive_count += 1
        
    return pos

def raid_session(wait_time=90, raid_type='britra', maxiter=30):
    """
    Complete raids.
    """
    team_pos = [settings.game_pos[0]+50, settings.game_pos[1]+125]
    if raid_type == 'inhibitor':
        team_pos[1] += 60
    elif raid_type == 'kraken':
        wait_time += 30
        team_pos[1] += 240
    
    for i in range(maxiter):
        # go to exploration status
        pos = search_loop("images/disturbance/explore.PNG", delay=5, maxiter=5)
        # check if exploration status found
        if not found_position(pos):
            print("Error: Cannnot find Exploration Status.")
            return
        click_and_delay(pos[0], pos[1], delay=0.5)

        # click on support request
        click_and_delay(settings.game_pos[0]+63, settings.game_pos[1]+215, delay=0.5)

        # click on a raid support
        pos = search_loop("images/disturbance/raid_support.PNG")
        if not found_position(pos):
            print("No more raids.")
            return
        click_and_delay(pos[0], pos[1], delay=.5)

        # click on prepare for battle
        pos = search_loop("images/disturbance/raid_prepare.PNG")
        click_and_delay(pos[0], pos[1], delay=.5)

        # wait for team page to pop up
        pos = search_loop("images/disturbance/raid_start.PNG")
        # select team
        click_and_delay(team_pos[0], team_pos[1], delay=0.5)
        # start raid
        click_and_delay(pos[0], pos[1], delay=.5)

        # wait for raid to finish
        time.sleep(wait_time)
        pos = search_loop("images/disturbance/explore.PNG", delay=10, maxiter=20)
        print(f"Complete {i+1} raid(s).")

#####################################################################
# Dailies.
##################################################################### 
def guild_donation():
    # move to guild page
    click_and_delay(settings.game_pos[0]+90, settings.game_pos[1]+82)

    # click donate
    pos = search_loop("images/daily/donate.PNG")
    click_and_delay(pos[0], pos[1])

    # click on gold
    click_and_delay(settings.game_pos[0]+440, settings.game_pos[1]+440)

#####################################################################
# Miscellaneous.
#####################################################################  
def salary_negotiate(type='blue', interval=2):
    """
    Level employees up. Default type is blue appraisal.
    """
    # select appraisal
    pos = [settings.game_pos[0]+740, settings.game_pos[1]+390] # blue appraisal position
    if type == 'brown': pos[0] -= 100
    if type == 'purple': pos[0] += 100
    pyautogui.moveTo(pos[0], pos[1])
    
    # hold down
    pyautogui.mouseDown()
    time.sleep(interval)
    pyautogui.mouseUp()
    # click negotation
    pyautogui.click(x=pos[0], y=pos[1]+130)

def npc_battle():
    """
    Do Gauntlet NPC battle.
    """
    # battle button
    click_and_delay(settings.game_pos[0]+600, settings.game_pos[1]+230, delay=1)
    # start battle
    pyautogui.doubleClick(settings.game_pos[0]+800, settings.game_pos[1]+510)
    # wait for battle to finish
    time.sleep(80)
    # exit out
    click_and_delay(settings.game_pos[0]+400, settings.game_pos[1]+300, delay=.5)

#####################################################################
# Logging and notification functions.
##################################################################### 
def print_dispatch_info(branches: list[Branch], iter, curr_time, totals, send_email=True, save_info=True):
    ticket_count = sim_count = quartz_count = 0

    for i in branches:
        if i.mission_type == CONTRACT:
            ticket_count += 1
        if i.mission_type == SIM:
            sim_count += 1
        if i.mission_type == QUARTZ:
            quartz_count += 1

    # save dispatch information if needed
    if save_info:
        with open('dispatch_log.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            end_date = curr_time.strftime("%m-%d-%Y %H:%M:%S")
            data = [end_date, settings.dive_count, ticket_count, sim_count, settings.raid_count]
            writer.writerow(data)
    
    # update totals
    totals[0] += settings.dive_count
    totals[1] += ticket_count
    totals[2] += sim_count
    totals[3] += quartz_count

    # get string of current time and time of next next dispatch
    end_time = curr_time.strftime("%H:%M:%S")
    t_next = curr_time + datetime.timedelta(seconds=2850) # 47.5 min
    next_time = t_next.strftime("%H:%M:%S")

    # print dispatch information
    info = ""
    info += f"Dispatch {iter} Complete: {end_time}\n"

    if settings.dive_count > 0:
        info += f"Dives found: {settings.dive_count}\n"
    if settings.raid_count > 0:
        info += f"Raids found: {settings.raid_count}\n"
    if ticket_count > 0:
        info += f"Employee Contracts found: {ticket_count}\n"
    if sim_count > 0:
        info += f"Simulation Permits found: {sim_count}\n"
    if quartz_count > 0:
        info += f"Quartz found: {quartz_count*60}\n"
    
    info += f"Total Dives: {totals[0]}\t Contracts: {totals[1]}\tPermits: {totals[2]}\n"
    info += f"Approximate Next Dispatch: {next_time}\n"

    # send info email
    if send_email:
        text = "\n" + info
        send_mail(text)

    info += "-----\n"
    print(info)

    settings.dive_count = settings.raid_count = 0
