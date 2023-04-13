import curses
import schedule
import time
import schedule

def start_scheduler():
    def write_file_with_array(new_value):
        # Your code to write to the .xmrig.json file with the given array

        with open('.xmrig.json', 'r+') as file:
            data = file.readlines()
            for i, line in enumerate(data):
                if '"rx":' in line:
                    data[i] = '\t\t"rx": ' + str(new_value) + ',\n'
                    break
            stdscr.addstr('Thread usage changed successfully')
            file.seek(0)
            file.writelines(data)
            file.truncate()

    def schedule_file_writes(array, time_of_day, array_2, time_of_day_2):
        # Schedule file writes for specified time of day
        schedule.every().day.at(time_of_day).do(write_file_with_array, new_value=array)
        schedule.every().day.at(time_of_day_2).do(write_file_with_array, new_value=array_2)

        while True:
            schedule.run_pending()
            time.sleep(1)

    original_array = [0, 8, 1, 9, 2, 10, 3, 11, 4, 12, 5, 13, 6, 14, 7, 15]

    stdscr.addstr('Please specify the first of day you want the program to change the thread count at >>> ')
    stdscr.refresh()
    curses.echo()
    time_of_day = stdscr.getstr().decode()
    curses.noecho()
    stdscr.addstr('Specify the amount of threads you want the program to start using at ' + time_of_day+ ' >>> ')
    stdscr.refresh()
    curses.echo()
    thread_count = int(stdscr.getstr().decode())
    curses.noecho()
    array = original_array[:thread_count]

    stdscr.addstr('Please specify the other time of day you want the program to change the thread count at >>> ')
    stdscr.refresh()
    curses.echo()
    time_of_day_2 = stdscr.getstr().decode()
    curses.noecho()
    stdscr.addstr('Specify the amount of threads you want the program to start using at ' + time_of_day_2+ ' >>> ')
    stdscr.refresh()
    curses.echo()
    thread_count = int(stdscr.getstr().decode())
    curses.noecho()
    array_2 = original_array[:thread_count]

    schedule_file_writes(array, time_of_day, array_2, time_of_day_2)


def manual_thread_count():
    # Set up the window
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    stdscr.clear()

    original_array = [0, 8, 1, 9, 2, 10, 3, 11, 4, 12, 5, 13, 6, 14, 7, 15]

    # Ask the user for number of threads
    stdscr.addstr('Please specify the number of threads you want to use >>> ')
    stdscr.refresh()  # Refresh the screen to show the prompt
    curses.echo()
    thread_count = int(stdscr.getstr().decode())
    curses.noecho()

    array = original_array[:thread_count]

    # Write the array to .xmrig.json file
    with open('.xmrig.json', 'r+') as file:
        data = file.readlines()
        for i, line in enumerate(data):
            if '"rx":' in line:
                data[i] = '\t\t"rx": ' + str(array) + ',\n'
                break
        stdscr.addstr('Thread count successfully set to ' + str(thread_count))
        file.seek(0)
        file.writelines(data)
        file.truncate()

# define the menu options
menu_options = ['Start scheduler', 'Manually increase / reduce thread count', 'Quit']

# define the functions to call for each option
menu_functions = ['start_scheduler()', 'manual_thread_count()', 'quit()']

# initialize the curses module
stdscr = curses.initscr()

# disable input echoing and enable special key interpretation
curses.noecho()
stdscr.keypad(True)

# set the current menu selection to the first option
current_option = 0

while True:
    # clear the screen and draw the menu options
    stdscr.clear()
    stdscr.addstr("Shitty monero scheduler thing v0.1\n")

    # draw the menu options, highlighting the current selection
    for i, option in enumerate(menu_options):
        if i == current_option:
            stdscr.addstr("> ")
        else:
            stdscr.addstr("  ")
        stdscr.addstr("[{}] {}\n".format(i+1, option))

    # wait for a key press
    key = stdscr.getch()

    # check if the key is an arrow key
    if key == curses.KEY_UP:
        # up arrow key pressed
        current_option = (current_option - 1) % len(menu_options)
    elif key == curses.KEY_DOWN:
        # down arrow key pressed
        current_option = (current_option + 1) % len(menu_options)
    elif key == ord('\n'):
        # enter key pressed
        selected_option = menu_options[current_option]
        exec(menu_functions[current_option]) # call the corresponding function
        if current_option == len(menu_options) - 1:  # quit if 'Quit' was selected
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()

            quit()

        stdscr.getch()  # wait for user to press a key before redrawing the menu

# restore the terminal to its normal state
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
