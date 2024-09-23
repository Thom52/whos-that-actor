import requests
import os
import time
import sys
import colorama

from dotenv import load_dotenv
from colorama import Fore, Style


load_dotenv()
api_key = os.getenv("MY_API_KEY")

if not api_key:
    raise ValueError("\nAPI key not found. Make sure it's set in the environment.\n")

BASE_URL = 'https://api.themoviedb.org/3'


def search_actor(actor_name):
    """
    Search TMDB for the value given in the input.
    Try and except statement to catch any errors.
    """
    
    try:
        search_url = f"{BASE_URL}/search/person"
        search_params = {
            'api_key': api_key,
            'query': actor_name
        }

        response = requests.get(search_url, params=search_params)
        response.raise_for_status()

        data = response.json()

        if data['total_results'] == 0:
            typingPrint(Fore.RED + f"\nActor '{actor_name}' cannot be not found.\n" + Style.RESET_ALL)
            return None

        actor = data['results'][0]
        return actor
    
    except requests.exceptions.RequestException as e:
        typingPrint(Fore.RED + f"\nError: Unable to fetch data due to network issues: {e}\n")
    except ConnectionError as ce:
        typingPrint(Fore.RED + f"\nFailed to connect to the API: {ce}\n" + Style.RESET_ALL)
    except TimeoutError as te:
        typingPrint(Fore.RED + f"\nAPI request timed out: {te}\n" + Style.RESET_ALL)
    except Exception as e:
        typingPrint(Fore.RED + f"\nAn error occurred during actor search: {e}\n" + Style.RESET_ALL)
    return None



def display_actor_info(actor):
    """
    Display the basic information about the actor retrieved from TMDB
    from the search_actor function.
    """

    try:
        typingPrint(Fore.LIGHTMAGENTA_EX + "\n--- Actor Information ---\n" + Style.RESET_ALL)
        typingPrint(Fore.BLUE + f"\nName: {actor.get('name')}\n" + Style.RESET_ALL)
        typingPrint(Fore.BLUE + f"\nProfile: https://www.themoviedb.org/person/{actor['id']}\n" + Style.RESET_ALL)

    except KeyError as ke:
        typingPrint(Fore.RED + f"\nMissing actor information: {ke}\n" + Style.RESET_ALL)
    except Exception as e:
        typingPrint(Fore.RED + f"\nError while displaying actor information: {e}\n" + Style.RESET_ALL)



def get_actor_filmography(actor_id):
    """
    Search for the filmography of the actor using their TMDB ID.
    Try and except statement to catch any errors.
    """

    try:
        filmography_url = f"{BASE_URL}/person/{actor_id}/movie_credits"
        film_params = {
            'api_key': api_key
        }

        response = requests.get(filmography_url, params=film_params)
        response.raise_for_status()

        data = response.json()
        
        filmography = data.get('cast', [])

        # Grabs filmography data and sorts it to display it in newest to oldest order.
        # 1900-01-01 is to make sure any movies without a date are displayed at bottom
        # of the list without causing any errors.
        filmography.sort(key=lambda movie: movie.get('release_date', '1900-01-01'), reverse=True)

        return filmography


    except requests.exceptions.RequestException as e:
        typingPrint(Fore.RED + f"\nError: Unable to fetch filmography due to network issues: {e}\n" + Style.RESET_ALL)
    except ConnectionError as ce:
        typingPrint(Fore.RED + f"\nFailed to connect to the API: {ce}\n" + Style.RESET_ALL)
    except TimeoutError as te:
        typingPrint(Fore.RED + f"\nAPI request timed out: {te}\n" + Style.RESET_ALL)
    except Exception as e:
        typingPrint(Fore.RED + f"\nAn unexpected error occurred while fetching the filmography: {e}\n" + Style.RESET_ALL)
    return None



def display_filmography(filmography):
    """
    Display the actor's filmography retrieved from TMDB
    from the get_actor_filmography function.
    """

    try:
        if not filmography:
            typingPrint(Fore.RED + "\nNo filmography found.\n" + Style.RESET_ALL)
            return

        # A while loop to loop through the filmography data and display it in
        # groups od 10. Then asks the user if they would like the next 10 
        # films to be displayed.
        all_films = len(filmography)
        begin = 0
        while begin < all_films:
            finish = min(begin + 10, all_films)
            typingPrint(Fore.LIGHTMAGENTA_EX + "\n--- Filmography ---\n" + Style.RESET_ALL)
            for movie in filmography[begin:finish]:
                title = movie.get('title')
                release_date = movie.get('release_date', 'N/A')
                character = movie.get('character', 'N/A')
                typingPrint(Fore.BLUE + f"\n{title} ({release_date}) - Character: {character}\n" + Style.RESET_ALL)

            begin += 10

            if begin < all_films:
                more = typingInput(Fore.GREEN + "\nWould you like to see the next 10 films? (y/n) " + Style.RESET_ALL).lower()
                if more != 'y':
                    break

    except Exception as e:
        typingPrint(Fore.RED + f"\nError while displaying filmography: {e}\n" + Style.RESET_ALL)



# Functions to create a typing effect in the terminal which replaces the
# print() and input() functions where desired.
# Code adapted from: https://www.101computing.net/python-typing-text-effect/
def typingPrint(text):
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.015)
print()

def typingInput(text):
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.035)
  return input()



# Uses os to clear terminal when conditions met.
# Code apadated from: https://www.101computing.net/python-typing-text-effect/
def clear_Screen():
    # Clear the terminal based on the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and macOS
        os.system('clear')



# Main execution logic

# Loops the logic until a correct input is searched,
# and allows the user to keep searching for new actors
# until they prompt to leave.
while True:
    try:

        print(Fore.YELLOW + r'''     
        
 __      ___        _      _____ _         _       _      _          ___ _ 
 \ \    / / |_  ___( )___ |_   _| |_  __ _| |_    /_\  __| |_ ___ _ |__ \ |
  \ \/\/ /| ' \/ _ \/(_-<   | | | ' \/ _` |  _|  / _ \/ _|  _/ _ \ '_|/_/_|
   \_/\_/ |_||_\___/ /__/   |_| |_||_\__,_|\__| /_/ \_\__|\__\___/_| (_)(_)
                                                                           
        
        ''' + Style.RESET_ALL)

        actor_name = typingInput(Fore.GREEN + "Enter the name of the actor: " + Style.RESET_ALL)

        if not actor_name:
            raise ValueError(Fore.RED + "Input cannot be empty." + Style.RESET_ALL)

        actor = search_actor(actor_name)

        if actor:
            display_actor_info(actor)

            actor_id = actor['id']
            filmography = get_actor_filmography(actor_id)
            display_filmography(filmography)

            another_search = typingInput(Fore.GREEN + "\nWould you like to search for another actor? (y/n) " + Style.RESET_ALL).lower()
            if another_search == 'y':
                # Clears terminal
                clear_Screen()
            else:
                print(Fore.YELLOW + "\nUntil next time, may the force be with you!\n" + Style.RESET_ALL)
                # Keeps the above print statement on the terminal for 5 seconds
                # and then clears terminal.
                time.sleep(5.0)
                clear_Screen()
                break 

    # KeyboardInterrupt exception to leave program when executed.
    except KeyboardInterrupt:
        typingPrint(Fore.RED + "\n\nProgram interrupted by user. Exiting gracefully, like tears in the rain...\n\n" + Style.RESET_ALL)
        time.sleep(3.0)
        clear_Screen()
        break
    except Exception as e:
        print(Fore.RED + f"\nAn unexpected error occurred in the main program: {e}\n" + Style.RESET_ALL)