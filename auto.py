from imports import *
from branch import Branch
import csv

dive_count = 0
raid_count = 0
game_pos = [-1, -1] # stores position of game

def run_game(default=False, wait=60):
    """
    Start the game and go to World Map. 
    """
    # go to game icon
    if default:
        # click game icon
        pyautogui.moveTo(110, 230)
        pyautogui.doubleClick()
        rand_pause(2.5)

        # click start game
        pyautogui.moveTo(1410, 840)
        rand_pause(15)
        pyautogui.doubleClick()
        rand_pause(5)

        # go to world map
        pyautogui.moveTo(1601, 548) # click x button
        pyautogui.click()
        rand_pause(.5)
        pyautogui.moveTo(1522, 855) # click world map
        pyautogui.click(clicks=3, interval=.3)
    else:
        # click game icon
        pos = search_loop("images/startup/icon.PNG", maxiter=30)
        pyautogui.doubleClick(pos[0]+5, pos[1]+5)
        rand_pause(3, False)

        # click start game
        pos = search_loop("images/startup/game.PNG")
        rand_pause(wait)
        # check for update
        update = imagesearch("images/misc/confirm.PNG")
        # wait for game to update if there is one
        if found_position(update):
            pyautogui.click(update[0], update[1])
            time.sleep(200)
            # click into start game
            pyautogui.click(pos[0]+600, pos[1]+400)
            time.sleep(10)
        pyautogui.doubleClick(pos[0]+600, pos[1]+400)
        rand_pause(2)

        # click x button
        pos = search_loop("images/startup/x.PNG") 
        click_and_delay(pos[0]+5, pos[1]+5, delay=.5, rand=False)
        # go to world map
        pos = search_loop("images/startup/world_map.PNG")
        pyautogui.click(pos[0], pos[1], clicks=3, interval=.3)
    
    rand_pause(2)
    return pos

def initialize_branches(default=False):
    """
    Save positions of each branch.
    """
    branches = []
    branch_names = ["ADC-G1", "Chamber", "Campamento", "Front Bay", "Lotus", "Charade"]
    images = ["adcg1", "chamber", "campamento", "frontbay", "lotus", "charade"]
    default_pos = [[398, 199], [703, 185], [900, 350], [410, 466], [46, 307], [204, 161]]
    
    # get outclick position
    out_pos = [game_pos[0]+920, game_pos[1]+203] 
    if not default:
        # find rightmost branch 
        pos = search_loop("images/branch/campamento.PNG")
        # store outclick position   
        out_pos = [pos[0]+70, pos[1]-195]                 

    # get/save positions of each branch
    for i, name in enumerate(branch_names):
        if default:
            pos_x = game_pos[0] + default_pos[i][0]
            pos_y = game_pos[1] + default_pos[i][1]
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

def do_missions(branches: list[Branch], last=1):
    for branch in branches:
        branch.start_dispatch(last)

def complete_missions(branches: list[Branch]):
    for branch in branches:
        branch.complete_mission()

def complete_raids():
    pos = search_loop("images/disturbance/explore.PNG")         # exploration status
    click_and_delay(pos[0], pos[1], delay=0.5)
    pos = search_loop("images/disturbance/raid_history.PNG")    # click raid history
    click_and_delay(pos[0], pos[1], delay=0.5)
    click_and_delay(pos[0]+710, pos[1]+211, delay=0)            # click complete all
    pyautogui.moveTo(pos[0]+860, pos[1]-80)        
    pyautogui.click(clicks=5, interval=0.3)
    pos = search_loop("images/disturbance/explore_exit.PNG")
    click_and_delay(pos[0]+5, pos[1]+5, delay=0.5)              # exit exploration

def find_disturbances(default=False, do_raids=True, max_dives=5, sweep=True):
    """
    Search for dives/raids until there are no more. 
    """
    global dive_count

    for i in range(6):
        # go to exploration status
        if default:
            click_and_delay(843, 870, delay=0.1)
        else:
            pos = search_loop("images/disturbance/explore.PNG")
            # check if exploration status found
            if not found_position(pos):
                print("Error: Cannnot find Exploration Status.")
                return
            click_and_delay(pos[0], pos[1], delay=0.5)

        # search for raids
        pos = raid_support(do_raids)
        # no raids found? search for dives
        if not found_position(pos):
            if dive_count >= max_dives:
                pos = [-1, -1]
            else:
                pos = find_dives(sweep)
        # no disturbances found? finish find exploration
        if not found_position(pos):
            # exit exploration
            pos = search_loop("images/disturbance/explore_exit.PNG")
            click_and_delay(pos[0]+5, pos[1]+5, delay=0.5)              
            return

def raid_support(do_raid):
    global raid_count
    pos = search_loop("images/disturbance/raid.PNG", delay=0.2, maxiter=2, accuracy=0.85)

    # raid found? --> support request or delete
    if found_position(pos):
        if do_raid:
            click_and_delay(pos[0]+570, pos[1]+40, delay=.5)        # click go
            pos = search_loop("images/disturbance/support_req.PNG")
            click_and_delay(pos[0], pos[1], delay=.5)               # support request
            pos = search_loop("images/disturbance/raid_ok.PNG")
            click_and_delay(pos[0], pos[1], delay=.5)               # confirm
            pos = search_loop("images/dispatch/return.PNG")
            click_and_delay(pos[0], pos[1], delay=.5)               # return
        else:
            # click delete
            click_and_delay(pos[0]+570, pos[1], delay=.1)
            # confirm delete
            pos = search_loop("images/dispatch/ok.PNG")
            click_and_delay(pos[0], pos[1])
            # exit exploration tab
            pos = search_loop("images/disturbance/explore_exit.PNG")
            click_and_delay(pos[0], pos[1])           
        raid_count += 1 
    
    return pos

def find_dives(sweep):
    pos = search_loop("images/disturbance/dive.PNG", delay=0.2, maxiter=2)

    # complete dive if found
    if found_position(pos):
        click_and_delay(pos[0]+580, pos[1]+10, delay=3)
        do_dive(sweep_dive=sweep)
    
    return pos

def do_dive(default=False, sweep_dive=True):
    global dive_count

    if default:
        click_and_delay(1409, 933, .1, rand=False) # click sweep
        click_and_delay(1502, 946, .5)               # click start dive
    else:
        if sweep_dive:
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
        pos = search_loop("images/disturbance/explore.PNG", delay=15, maxiter=40)
        # dive not complete? exit --> probably shouldn't happen
        if not found_position(pos):
            print("dive error")
            exit_game()

        dive_count += 1

def exit_game(default=False):
    if default:
        click_and_delay(1719, 444, .01) # exit button
    else:
        pos = search_loop("images/misc/exit.PNG", maxiter=20)
        pyautogui.click(pos[0]+2, pos[1]+2)

def automize(maxiter=200, use_default=False, wait_error=60, raids=False, stop_time="3000-01-01 00:00:00"):
    global game_pos         # position of game
    totals = [0, 0, 0, 0]   # total dives, contracts, simulations, quartz found
    waiting = 2760          # 46 min.
    i = 1                   # dive iteration

    last_dispatch = False
    last_long = True        # true if last mission is 8-hour else 4-hour
    last_type = 8           # last mission type (default 8-hour)

    last_start, last_end = 1, 2     # time for 8-hour
    if not last_long:
        last_start, last_end = 4, 5 # time for 4-hour
        last_type = 4

    # buffer time
    time.sleep(.5)

    while i <= maxiter:
        # check time for last mission
        curr_time = datetime.datetime.now()
        target_time = datetime.datetime.strptime(stop_time, '%Y-%m-%d %H:%M:%S')
        if curr_time > target_time:
            last_dispatch = True

        # check for internet connection
        if no_internet():
            time.sleep(wait_error)
            continue

        # minimize any open windows
        minimize_windows()

        # random game start time (less sus O_O)
        rand_wait = random.uniform(0, 40)
        if i > 1: time.sleep(rand_wait)

        # first iteration wait less
        init_wait = 15 if i == 1 else 60

        # run the game
        pos = run_game(use_default, wait=init_wait)
        if not found_position(pos):
            # something went wrong with run game?
            print("Run game error.")
            exit_game()
            time.sleep(wait_error)
            continue
        # get game position (for default)
        pos = imagesearch("images/misc/game.PNG")
        game_pos = [pos[0], pos[1]]

        # complete wait time (47 min. 25 sec.)
        if i > 1: time.sleep(40 - rand_wait)

        # initialize all branches
        rand_pause(.5)
        branches = initialize_branches(default=True)
        # check if all branches initialized
        if len(branches) < 6:
            print("Could not initialize all branches.")
            exit_game()
            time.sleep(wait_error)
            continue

        # complete any finished raids
        if raids:
            complete_raids()
        else:
            time.sleep(4)

        # first iteration, complete any dives left over
        if i == 1: find_disturbances(do_raids=False, sweep=False)

        # get dispatch rewards
        complete_missions(branches)
        rand_pause(0.1)

        # start new dispatch
        if last_dispatch:
            do_missions(branches, last=last_type)
        else:
            do_missions(branches)

        # get time finished dispatch missions
        t = datetime.datetime.now()

        # complete any disturbances found
        start = time.time()
        num_dives = 5
        # if sleeping, don't do dives
        if sleep_time(t.time()):
            num_dives = 5
        find_disturbances(do_raids=raids, sweep=False, max_dives=num_dives)
        exit_game()
        # print dispatch information
        print_info(branches, i, t, totals)
        end = time.time()

        # if last mission: don't need to wait
        if last_dispatch:
            break
        # wait until next dispatch
        wait_time = waiting - (end - start)
        time.sleep(wait_time) 
        i += 1

    # shut down the pc
    shut_down()

def print_info(branches: list[Branch], iter, curr_time, totals, send_email=True, save_info=True):
    global dive_count, raid_count
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
        with open('log.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            end_date = curr_time.strftime("%m-%d-%Y %H:%M:%S")
            data = [end_date, dive_count, ticket_count, sim_count, raid_count]
            writer.writerow(data)
    
    # update totals
    totals[0] += dive_count
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

    if dive_count > 0:
        info += f"Dives found: {dive_count}\n"
    if raid_count > 0:
        info += f"Raids found: {raid_count}\n"
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

    dive_count = raid_count = 0


def main():
    pyautogui.FAILSAFE = False # move mouse to upper left to abort
    
    automize(raids=False, stop_time="2025-08-22 23:50:00")

    # pos = search_loop("images/dispatch/ongoing.PNG", delay=0.2, maxiter=2, accuracy=0.85)
    # print(pos)
    # pyautogui.moveTo(pos)
    # minimize_windows()
    # global game_pos
    # pos = imagesearch("images/misc/game.PNG")
    # game_pos = [pos[0], pos[1]]
    # pyautogui.moveTo(game_pos[0]+900, game_pos[1]+350)
    # branches = initialize_branches(default=True)
    # complete_missions(branches)
    # do_missions(branches)
    # find_disturbances()
    # print_info(branches)
    # pos = search_loop("images/disturbance/raid.PNG", delay=0.2, maxiter=2, accuracy=0.85)   
    # click_and_delay(pos[0]+570, pos[1], delay=.1)
    # pos = search_loop("images/dispatch/ok.PNG")
    # click_and_delay(pos[0], pos[1])

if __name__ == "__main__":
    main()