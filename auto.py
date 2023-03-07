from imports import *
from branch import Branch
import csv

dive_count = 0
raid_count = 0

def run_game(default=False):
    """
    Start the game and go to World Map. 
    """
    use_default = default       # use default locations
    pos = pyautogui.position()  # position of mouse

    # go to game icon
    if use_default:
        # click game icon
        pyautogui.moveTo(110, 230)
        pyautogui.doubleClick()
        time.sleep(rand_pause(2.5))

        # click start game
        pyautogui.moveTo(1410, 840)
        time.sleep(rand_pause(15))
        pyautogui.doubleClick()
        time.sleep(rand_pause(5))

        # go to world map
        pyautogui.moveTo(1601, 548) # click x button
        pyautogui.click()
        time.sleep(rand_pause(.5))
        pyautogui.moveTo(1522, 855) # click world map
        pyautogui.click(clicks=2, interval=rand_pause(.3))
    else:
        # click game icon
        pos = goto_image("icon", "images/startup/icon.PNG")
        pyautogui.move(5, 5)
        pyautogui.doubleClick()
        time.sleep(5)

        # click start game
        pos = goto_image("game", "images/startup/game.PNG")
        time.sleep(rand_pause(15))
        pyautogui.move(600, 400)
        pyautogui.doubleClick()
        time.sleep(rand_pause(5))

        # go to world map
        pos = goto_image("x", "images/startup/x.PNG") # click x button
        pyautogui.move(5, 5)
        pyautogui.click()
        time.sleep(rand_pause(.5))
        pos = goto_image("world map", "images/startup/world_map.PNG")
        pyautogui.click(clicks=2, interval=rand_pause(.1))
    
    time.sleep(rand_pause(3))

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
    pos = goto_image("right most branch", "images/branch/campamento.PNG")
    pyautogui.move(70, -195)
    pos = pyautogui.position()
    out_pos = [pos[0], pos[1]]

    for i, name in enumerate(branch_names):
        if default:
            branches.append(Branch(name, default_pos[i]))
        else:
            path = "images/branch/" + images[i] + ".PNG"
            pos = goto_image(images[i], path)
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
            delay_click(843, 870, 0.1)
        else:
            pos = goto_image("explore", "images/disturbance/explore.PNG")
            delay_click(pos[0], pos[1], 0.1)

        time.sleep(0.3)
        pos = find_dives()
        if pos[0] == -1:
            return

def find_dives():
    pos = scroll_find("images/disturbance/dive.PNG")

    if pos[0] != -1:
        delay_click(pos[0]+580, pos[1]+10, .5)
        time.sleep(rand_pause(3))
        do_dive()
    
    return pos

def do_dive(default=False):
    global dive_count

    if default:
        delay_click(1409, 933, .1, random=False) # click sweep
        delay_click(1502, 946, .5)               # click start dive
    else:
        pos = goto_image("sweep", "images/disturbance/sweep.PNG")
        delay_click(pos[0]+15, pos[1]+15, .1, random=False)

        pos = goto_image("start", "images/disturbance/start_dive.PNG")
        delay_click(pos[0], pos[1], .5)
    
    dive_count += 1 # increment dive count
    time.sleep(rand_pause(150))

def exit_game(default=False):
    if default:
        delay_click(1719, 444, .01) # exit button
    else:
        pos = imagesearch("images/misc/exit.PNG")
        pos = goto_image("game", "images/misc/exit.PNG")
        delay_click(pos[0]+2, pos[1]+2, 0, random=False)

def minimize_vscode(default=False):
    pos = goto_image("minimize", "images/misc/minimize.PNG")
    pyautogui.click()
    rand_pause(.3)

def automize(maxiter=20, use_default=False):
    waiting = 2850 # 47.5 min.
    minimize_vscode()
    
    for i in range(maxiter):
        run_game(use_default)
        branches = initialize_branches(use_default)

        complete_missions(branches)
        do_missions(branches)

        start = time.time()
        find_disturbances(use_default)
        print_info(branches)
        exit_game(use_default)
        end = time.time()

        new_wait = waiting - (end - start)
        time.sleep(new_wait)

def print_info(branches: list[Branch]):
    global dive_count, raid_count
    ticket_count = quartz_count = 0

    for i in branches:
        if i.mission_type == CONTRACT:
            ticket_count += 1
        if i.mission_type == QUARTZ:
            quartz_count += 1

    # save info
    # with open('log.csv', 'a', encoding='UTF8', newline='') as f:
    #     writer = csv.writer(f)
    #     data = [ticket_count, quartz_count, dive_count, raid_count]
    #     writer.writerow(data)

    # print info
    print("Dispatch Compelete")

    if dive_count > 0:
        print(f"Dives found: {dive_count}")
    if raid_count > 0:
        print(f"Raids found: {raid_count}")
    if ticket_count > 0:
        print(f"Employee Contracts found: {ticket_count}")
    if quartz_count > 0:
        print(f"Quartz found: {quartz_count*60}")
    print("----")

    dive_count = raid_count = 0


def main():
    pyautogui.FAILSAFE = True # move mouse to upper left to abort
    while True:
        automize()
        exit_game
        time.sleep(60)

    # minimize_vscode()
    # branches = initialize_branches()
    # complete_missions(branches)
    # do_missions(branches)
    # find_disturbances()
    # print_info(branches)


if __name__ == "__main__":
    main()