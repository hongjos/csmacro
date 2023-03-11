from imports import *
from branch import Branch
import csv

dive_count = 0
raid_count = 0

def run_game(default=False):
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
        pos = search_loop("images/startup/icon.PNG")
        pyautogui.doubleClick(pos[0]+5, pos[1]+5)
        rand_pause(3, False)

        # click start game
        pos = search_loop("images/startup/game.PNG")
        rand_pause(15)
        pyautogui.doubleClick(pos[0]+600, pos[1]+400)
        rand_pause(2)

        # go to world map
        pos = search_loop("images/startup/x.PNG") # find x button
        click_and_delay(pos[0]+5, pos[1]+5, delay=.5, rand=False)
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
    default_pos = [[1205, 669], [1512, 657], [1669, 840], 
                   [1217, 939], [852, 779], [1009, 631]]
    
    # get outclick
    pos = search_loop("images/branch/campamento.PNG")   # find rightmost branch
    out_pos = [pos[0]+70, pos[1]-195]                   # store outclick position

    for i, name in enumerate(branch_names):
        if default:
            branches.append(Branch(name, default_pos[i]))
        else:
            path = "images/branch/" + images[i] + ".PNG"
            pos = search_loop(path)
            # add branch if found
            if pos[0] != -1:
                pyautogui.moveTo(pos[0], pos[1])
                position = [pos[0]+10, pos[1]-30]
                branches.append(Branch(name, position, out_pos))
    
    return branches

def do_missions(branches: list[Branch]):
    for branch in branches:
        branch.start_dispatch()

def complete_missions(branches: list[Branch]):
    for branch in branches:
        branch.complete_mission()

def find_disturbances(default=False):
    """
    Search for dives/raids until there are no more. 
    """
    for i in range(6):
        # go to exploration status
        if default:
            click_and_delay(843, 870, delay=0.1)
        else:
            pos = search_loop("images/disturbance/explore.PNG")
            # check if exploration status found
            if pos[0] == -1:
                print("Error: Cannnot find Exploration Status.")
                return
            click_and_delay(pos[0], pos[1], delay=0.5)

        pos = find_dives()
        # no disturbances found, finish find exploration
        if pos[0] == -1:
            return

def find_dives():
    pos = scroll_find("images/disturbance/dive.PNG")

    # dive found? --> sweep it
    if pos[0] != -1:
        click_and_delay(pos[0]+580, pos[1]+10, delay=3)
        do_dive()
    
    return pos

def do_dive(default=False):
    global dive_count

    if default:
        click_and_delay(1409, 933, .1, rand=False) # click sweep
        click_and_delay(1502, 946, .5)               # click start dive
    else:
        pos = search_loop("images/disturbance/sweep.PNG")
        # only sweep if sweep button found
        if pos[0] != -1:
            click_and_delay(pos[0]+15, pos[1]+15, delay=.1, rand=False)
            # start dive
            pos = search_loop("images/disturbance/start_dive.PNG")
            if pos[0] == -1:
                # this shouldn't happen but exit game just in case
                exit_game()
                return
            click_and_delay(pos[0], pos[1], delay=150) # click and wait for dive to finish
            dive_count += 1

def exit_game(default=False):
    if default:
        click_and_delay(1719, 444, .01) # exit button
    else:
        pos = search_loop("images/misc/exit.PNG", maxiter=20)
        pyautogui.click(pos[0]+2, pos[1]+2)

def automize(maxiter=100, use_default=False, wait_error=60):
    totals = [0, 0, 0]  # total dives, contracts, quartz found
    waiting = 2850      # 47.5 minutes
    i = 1

    while i <= maxiter:
        # check for internet connection
        if no_internet():
            time.sleep(wait_error)
            continue

        minimize_windows()
        pos = run_game(use_default)
        # something went wrong with run game?
        if pos[0] == -1:
            print("Run game error.")
            exit_game()
            time.sleep(wait_error)
            continue

        rand_pause(2)
        branches = initialize_branches(use_default)
        # check if all branches initialized
        if len(branches) < 6:
            print("Could not initialize all branches.")
            exit_game()
            time.sleep(wait_error)
            continue

        rand_pause(0.1)
        complete_missions(branches)
        rand_pause(0.1)
        do_missions(branches)
        # get time finished branches
        t = datetime.datetime.now()

        start = time.time()
        find_disturbances(use_default)
        exit_game(use_default)
        print_info(branches, i, t, totals)
        end = time.time()

        # wait until next dispatch
        wait_time = waiting - (end - start)
        time.sleep(wait_time) 
        i += 1

def print_info(branches: list[Branch], iter, curr_time, totals, send_email=True, save_info=False):
    global dive_count, raid_count
    ticket_count = quartz_count = 0

    for i in branches:
        if i.mission_type == CONTRACT:
            ticket_count += 1
        if i.mission_type == QUARTZ:
            quartz_count += 1

    # save dispatch information if needed
    if save_info:
        with open('log.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            data = [ticket_count, quartz_count, dive_count, raid_count]
            writer.writerow(data)
    
    # update totals
    totals[0] += dive_count
    totals[1] += ticket_count
    totals[2] += quartz_count

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
    if quartz_count > 0:
        info += f"Quartz found: {quartz_count*60}\n"
    
    info += f"Total Dives: {totals[0]}\t Contracts: {totals[1]}\tQuartz: {totals[2]*60}\n"
    info += f"Approximate Next Dispatch: {next_time}\n"

    if send_email:
        send_email(info)

    info += "-----\n"
    print(info)

    dive_count = raid_count = 0


def main():
    pyautogui.FAILSAFE = False # move mouse to upper left to abort
    
    automize()

    # minimize_windows()
    # pos = imagesearch("images/branch/adcg1.PNG")
    # branches = initialize_branches()
    # complete_missions(branches)
    # do_missions(branches)
    # find_disturbances()
    # print_info(branches)


if __name__ == "__main__":
    main()