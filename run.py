import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("MY_API_KEY")

if not api_key:
    raise ValueError("API key not found. Make sure it's set in the environment.")

BASE_URL = 'https://api.themoviedb.org/3'
