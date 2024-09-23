import time

from colorama import Fore, Style
from utils import clear_screen, typing_input, typing_print
from actor import (
    get_actor_filmography,
    display_actor_info,
    display_filmography,
    search_actor,
)

# Main execution logic
if __name__ == "__main__":
    # Loops the logic until a correct input is searched,
    # and allows the user to keep searching for new actors
    # until they prompt to leave.
    while True:
        try:

            print(
                Fore.YELLOW
                + r"""
    __      ___        _      _____ _         _       _      _          ___ _
    \ \    / / |_  ___( )___ |_   _| |_  __ _| |_    /_\  __| |_ ___ _ |__ \ |
     \ \/\/ /| ' \/ _ \/(_-<   | | | ' \/ _` |  _|  / _ \/ _|  _/ _ \ '_|/_/_|
      \_/\_/ |_||_\___/ /__/   |_| |_||_\__,_|\__| /_/ \_\__|\__\___/_| (_)(_)
            """
                + Style.RESET_ALL
            )

            actor_name = typing_input(
                Fore.GREEN
                + "\nEnter the name of the actor: "
                + Style.RESET_ALL
            )

            if not actor_name:
                raise ValueError(
                    Fore.RED
                    + "Input cannot be empty."
                    + Style.RESET_ALL)

            actor = search_actor(actor_name)

            if actor:
                display_actor_info(actor)

                actor_id = actor["id"]
                filmography = get_actor_filmography(actor_id)
                display_filmography(filmography)

                another_search = typing_input(
                    Fore.GREEN
                    + "\nWould you like to search for another actor? (y/n) "
                    + Style.RESET_ALL
                ).lower()
                if another_search == "y":
                    # Clears terminal
                    clear_screen()
                else:
                    print(
                        Fore.YELLOW
                        + "\nUntil next time, may the force be with you!\n"
                        + Style.RESET_ALL
                    )
                    # Keeps the above print statement on the terminal
                    # for 5 seconds and then clears terminal.
                    time.sleep(5.0)
                    clear_screen()
                    break

        # KeyboardInterrupt exception to leave program when executed.
        except KeyboardInterrupt:
            typing_print(
                Fore.RED
                + "\n\nExiting gracefully, like tears in the rain...\n\n"
                + Style.RESET_ALL
            )
            time.sleep(3.0)
            clear_screen()
            break
        except Exception as e:
            print(
                Fore.RED
                + f"\nAn unexpected error occurred in the main program: {e}\n"
                + Style.RESET_ALL
            )
