import requests
import os
import time

from dotenv import load_dotenv
from colorama import Fore, Style
from utils import clear_screen, typing_input, typing_print

load_dotenv()
api_key = os.getenv("MY_API_KEY")

if not api_key:
    raise ValueError("\nAPI key not found. Make sure it's set in the environment.\n")

BASE_URL = "https://api.themoviedb.org/3"



def search_actor(actor_name):
    """
    Search TMDB for an actor and only returns the first occurence from a list of actors
    """

    try:
        search_url = f"{BASE_URL}/search/person"
        search_params = {"api_key": api_key, "query": actor_name}

        response = requests.get(search_url, params=search_params)
        response.raise_for_status()

        data = response.json()

        if data["total_results"] == 0:
            typing_print(
                Fore.RED
                + f"\nActor '{actor_name}' cannot be not found.\n"
                + Style.RESET_ALL
            )
            return None

        actor = data["results"][0]
        return actor

    except requests.exceptions.RequestException as e:
        typing_print(
            Fore.RED + f"\nError: Unable to fetch data due to network issues: {e}\n"
        )
    except ConnectionError as ce:
        typing_print(
            Fore.RED + f"\nFailed to connect to the API: {ce}\n" + Style.RESET_ALL
        )
    except TimeoutError as te:
        typing_print(Fore.RED + f"\nAPI request timed out: {te}\n" + Style.RESET_ALL)
    except Exception as e:
        typing_print(
            Fore.RED
            + f"\nAn error occurred during actor search: {e}\n"
            + Style.RESET_ALL
        )
    return None


def display_actor_info(actor):
    """
    Display the basic information about the actor retrieved from TMDB
    """

    try:
        typing_print(
            Fore.LIGHTMAGENTA_EX + "\n--- Actor Information ---\n" + Style.RESET_ALL
        )
        typing_print(Fore.BLUE + f"\nName: {actor.get('name')}\n" + Style.RESET_ALL)
        typing_print(
            Fore.BLUE
            + f"\nProfile: https://www.themoviedb.org/person/{actor['id']}\n"
            + Style.RESET_ALL
        )

    except KeyError as ke:
        typing_print(
            Fore.RED + f"\nMissing actor information: {ke}\n" + Style.RESET_ALL
        )
    except Exception as e:
        typing_print(
            Fore.RED
            + f"\nError while displaying actor information: {e}\n"
            + Style.RESET_ALL
        )


def get_actor_filmography(actor_id):
    """
    Search for the filmography of the actor using their TMDB ID.
    """

    try:
        filmography_url = f"{BASE_URL}/person/{actor_id}/movie_credits"
        film_params = {"api_key": api_key}

        response = requests.get(filmography_url, params=film_params)
        response.raise_for_status()

        data = response.json()

        filmography = data.get("cast", [])

        # Grabs filmography data and sorts it to display it in newest to oldest order.
        # 1900-01-01 is to make sure any movies without a date are displayed at bottom
        # of the list without causing any errors.
        filmography.sort(
            key=lambda movie: movie.get("release_date", "1900-01-01"), reverse=True
        )

        return filmography

    except requests.exceptions.RequestException as e:
        typing_print(
            Fore.RED
            + f"\nError: Unable to fetch filmography due to network issues: {e}\n"
            + Style.RESET_ALL
        )
    except ConnectionError as ce:
        typing_print(
            Fore.RED + f"\nFailed to connect to the API: {ce}\n" + Style.RESET_ALL
        )
    except TimeoutError as te:
        typing_print(Fore.RED + f"\nAPI request timed out: {te}\n" + Style.RESET_ALL)
    except Exception as e:
        typing_print(
            Fore.RED
            + f"\nAn unexpected error occurred while fetching the filmography: {e}\n"
            + Style.RESET_ALL
        )
    return None


def display_filmography(filmography):
    """
    Display the actor's filmography retrieved from TMDB
    """

    try:
        if not filmography:
            typing_print(Fore.RED + "\nNo filmography found.\n" + Style.RESET_ALL)
            return

        # A while loop to loop through the filmography data and display it in
        # groups of 10. Then asks the user if they would like the next 10
        # films to be displayed.
        all_films = len(filmography)
        begin = 0
        while begin < all_films:
            finish = min(begin + 10, all_films)
            typing_print(
                Fore.LIGHTMAGENTA_EX + "\n--- Filmography ---\n" + Style.RESET_ALL
            )
            for movie in filmography[begin:finish]:
                title = movie.get("title")
                release_date = movie.get("release_date", "N/A")
                character = movie.get("character", "N/A")
                typing_print(
                    Fore.BLUE
                    + f"\n{title} ({release_date}) - Character: {character}\n"
                    + Style.RESET_ALL
                )

            begin += 10

            if begin < all_films:
                more = typing_input(
                    Fore.GREEN
                    + "\nWould you like to see the next 10 films? (y/n) "
                    + Style.RESET_ALL
                ).lower()
                if more != "y":
                    break

    except Exception as e:
        typing_print(
            Fore.RED + f"\nError while displaying filmography: {e}\n" + Style.RESET_ALL
        )

