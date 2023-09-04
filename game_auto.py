"""
File: game_auto.py
Description:
"""

from auto_utils import *

def dispatch_auto(maxiter=200, wait_error=60):
    """
    Automatically do dispatch missions, complete dives, and send raid supports.
    """
    totals = [0, 0, 0, 0]   # total dives, contracts, simulations, quartz found
    waiting = 2760          # 46 min.
    i = 1                   # dive iteration

    time.sleep(.5) # buffer

    while i <= maxiter:
        # get variables
        do_raids = bool(int(get_var('do_raids')))
        num_dives = int(get_var('num_dives'))
        last_dispatch = bool(int(get_var('last_dispatch')))

        # check time for last mission
        curr_time = datetime.datetime.now()
        stop_dispatch = get_var('stop_dispatch')
        stop_time = datetime.datetime.strptime(stop_dispatch, '%Y-%m-%d %H:%M:%S')
        if curr_time > stop_time:
            last_dispatch = True

        # check for internet connection
        if no_internet():
            time.sleep(wait_error)
            continue

        minimize_windows()

        # random game start time (less sus O_O)
        rand_wait = random.uniform(0, 40)
        if i > 1: time.sleep(rand_wait)

        # wait less for first iteration
        init_wait = 15 if i == 1 else 60

        # run the game and go to world map
        pos = run_game(startup_buffer=init_wait)
        pos = goto_world_map()
        if not found_position(pos):
            print("Error: Game Startup Failed")
            exit_game()
            time.sleep(wait_error)
            continue

        init_game_pos()

        # complete wait time (47 min. 25 sec.)
        if i > 1: time.sleep(40 - rand_wait)

        # initialize all branches
        rand_pause(.5)
        branches = initialize_branches(default=True)
        # check if all branches initialized
        if len(branches) < 6:
            print("Error: Branch Initialization Failure")
            exit_game()
            time.sleep(wait_error)
            continue

        # complete any finished raids
        if do_raids:
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
            do_missions(branches, mission_time=8)
        else:
            do_missions(branches)

        # get time finished dispatch missions
        t = datetime.datetime.now()

        # complete any disturbances found
        start = time.time()
        num_dives = 5
        find_disturbances(do_raids, max_dives=num_dives, sweep=False)
        exit_game()
        print_dispatch_info(branches, i, t, totals)
        end = time.time()

        # if last mission: don't need to wait
        if last_dispatch:           
            break
        # wait until next dispatch
        wait_time = waiting - (end - start)
        time.sleep(wait_time) 
        i += 1

    set_var('last_dispatch', 0) # set last dispatch back to false
    shut_down()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('type')
    args = parser.parse_args()

    pyautogui.FAILSAFE = False # move mouse to upper left to abort
    settings.init() # initialize global variables

    auto_type = args.type

    # default to auto dispatch
    if auto_type == 'dispatch':
        print("Starting dispatch...\n")
        dispatch_auto()
    elif auto_type == 'daily':
        print("Doing dailies...\n")
    elif auto_type == 'raid':
        print("Starting raid session...\n")
    else:
        print("huh...")

if __name__ == "__main__":
    main()