import sys
import os
import time

# Functions to create a typing effect in the terminal which replaces the
# print() and input() functions where desired.
# Code adapted from: https://www.101computing.net/python-typing-text-effect/
def typing_print(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.015)
print()


def typing_input(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.035)
    return input()


# Uses os to clear terminal when conditions met.
# Code apadated from: https://www.101computing.net/python-typing-text-effect/
def clear_screen():
    # Clear the terminal based on the operating system
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Linux and macOS
        os.system("clear")

