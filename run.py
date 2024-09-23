import requests
from dotenv import load_dotenv
import os

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
            print(f"\nActor '{actor_name}' cannot be not found.\n")
            return None

        actor = data['results'][0]
        return actor
    
    except requests.exceptions.RequestException as e:
        print(f"\nError: Unable to fetch data due to network issues: {e}\n")
    except ConnectionError as ce:
        print(f"\nFailed to connect to the API: {ce}\n")
    except TimeoutError as te:
        print(f"\nAPI request timed out: {te}\n")
    except Exception as e:
        print(f"\nAn error occurred during actor search: {e}\n")
    return None



def display_actor_info(actor):
    """
    Display the basic information about the actor retrieved from TMDB
    from the search_actor function.
    """

    try:
        print("\n--- Actor Information ---\n")
        print(f"Name: {actor.get('name')}")
        print(f"Known For: {', '.join([movie['title'] for movie in actor.get('known_for', [])])}")
        print(f"Profile: https://www.themoviedb.org/person/{actor['id']}\n")
    
    except KeyError as ke:
        print(f"\nMissing actor information: {ke}\n")
    except Exception as e:
        print(f"\nError while displaying actor information: {e}\n")



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
        return (data['cast']) 

    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to fetch filmography due to network issues: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while fetching the filmography: {e}")
    return None



def display_filmography(filmography):
    """
    Display the actor's filmography retrieved from TMDB
    from the get_actor_filmography function.
    """

    try:
        if not filmography:
            print("No filmography found.")
            return

        print("\n--- Filmography ---\n")
        for movie in filmography:
            title = movie.get('title')
            release_date = movie.get('release_date', 'N/A')
            character = movie.get('character', 'N/A')
            print(f"{title} ({release_date}) - Character: {character}\n")

    except Exception as e:
        print(f"Error while displaying filmography: {e}")



try:
    actor_name = input("Enter the name of the actor: ")

    if not actor_name:
        raise ValueError("Input cannot be empty.")

    actor = search_actor(actor_name)

    if actor:
        display_actor_info(actor)

        actor_id = actor['id']
        filmography = get_actor_filmography(actor_id)
        display_filmography(filmography)

except Exception as e:
    print(f"\nAn unexpected error occurred in the main program: {e}\n")