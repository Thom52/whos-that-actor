import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("MY_API_KEY")

if not api_key:
    raise ValueError("API key not found. Make sure it's set in the environment.")

BASE_URL = 'https://api.themoviedb.org/3'



def search_actor(actor_name):
    """
    Search TMDB for the value given in the input.
    try and except statement to catch any errors.
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
            print(f"No actor found with the name '{actor_name}'.")
            return None

        actor = data['results'][0]
        return actor

    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to fetch data due to network issues: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None



def display_actor_info(actor):
    """
    Fetch and display the basic information about the actor retrieved from TMDB.
    """

    try:
        print("\n--- Actor Information ---\n")
        print(f"Name: {actor.get('name')}")
        print(f"Known For: {', '.join([movie['title'] for movie in actor.get('known_for', [])])}")
        print(f"Profile: https://www.themoviedb.org/person/{actor['id']}\n")
    except Exception as e:
        print(f"Error while displaying actor information: {e}")


actor_name = input("Enter the name of the actor: ")
actor = search_actor(actor_name)
display_actor_info(actor)