import requests
import random

class AnimeAPI:
    """
    A class to interact with multiple Anime APIs and retrieve information about episodes and streams.

    Attributes:
        base_urls (list): List of base endpoints for multiple Anime APIs
    """

    def __init__(self):
        self.base_urls = [
            "https://consumet-private.vercel.app/anime/zoro",
            "https://animeleech.vercel.app/anime/zoro",
            # Add more API endpoints here
        ]

    def get_random_base_url(self):
        return random.choice(self.base_urls)

    def get_episodes(self, id):
        base_url = self.get_random_base_url()
        response = requests.get(f"{base_url}/info?id={id}").json()
        return response.get("episodes", [])

    def get_info(self, id, key):
        base_url = self.get_random_base_url()
        response = requests.get(f"{base_url}/info?id={id}").json()
        return response.get(key, "")

    def get_watch_info(self, episode_id):
        base_url = self.get_random_base_url()
        response = requests.get(f"{base_url}/watch?episodeId={episode_id}").json()
        return response
