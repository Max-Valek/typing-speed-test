import curses
from curses import wrapper
import time
import random

# Initiate start screen
def start_screen(stdscr):
    stdscr.clear() # clear the screen
    stdscr.addstr(0, 0, "Welcome to the Speed Typing Test!") # like print() at row 0, column 0 (start of first line)
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh() # refresh the screen
    stdscr.getkey() # get key inputted by user

def display_text(stdscr, target, current, wpm=0):
        stdscr.addstr(target)
        stdscr.addstr(1, 0, f"WPM: {wpm}") # 1, 0 is one row down from other text

        for i, char in enumerate(current): # loop through chars and their indeces in the current_text list
            correct_char = target[i]
            color = curses.color_pair(1) # green

            if char != correct_char: # if incorrect char is typed, change color to red
                color = curses.color_pair(2)

            stdscr.addstr(0, i, char, color)

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines() # list of all lines in the file
        return random.choice(lines).strip() # random.choice randomly chooses one item (line) from a list, strip removes \n from the end of the lines (or any other whitespace)

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True) # do not delay while waiting for user hit a key

    while True:
        time_elapsed = max(time.time() - start_time, 1) # to avoid dividing by zero, returns 1 if less than 1
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        # end the game when user has typed the correct target text
        if "".join(current_text) == target_text: # .join will convert the target_text string into a list
            stdscr.nodelay(False)
            break # leave while loop

        # getkey() will throw an exception if a user does not enter a key
        try:
            key = stdscr.getkey() # this is a "block" function, meaning it does nothing until user presses a key (need the nodelay function)
        except:
            continue # bring back to the top of the while loop

        if ord(key) == 27: # ascii value for the escape key
            break
        
        if key in ("KEY_BACKSPACE", '\b', "\x7f"): # checking if backspace is pressed (different vals for different OS)
            if len(current_text) > 0:
                current_text.pop() # removes last element from current_text
        elif len(current_text) < len(target_text): # ensures that you dont type beyond the length of the target text
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # pair of green fg (text) and white bg has id of 1
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) # red fg (text) and black bg
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK) # white text, black bg
    
    start_screen(stdscr)

    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to play again... (or esc to quit)")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main)