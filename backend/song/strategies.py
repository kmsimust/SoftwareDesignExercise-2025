from abc import ABC, abstractmethod
import requests
from django.conf import settings
import json

class SongGeneratorStrategy(ABC):
    @abstractmethod
    def generate_song(self, song):
        """
        Generate a song for the given song instance.
        Should update song.task_id, song.generation_status, and song.audio_url as appropriate.
        """
        pass

    @abstractmethod
    def check_status(self, song):
        """
        Check the status of song generation.
        Should update song.generation_status and song.audio_url if complete.
        """
        pass


class MockSongGeneratorStrategy(SongGeneratorStrategy):
    def generate_song(self, song):
        # Mock implementation - no external API call
        song.task_id = "mock-task-123"
        song.generation_status = "SUCCESS"
        song.audio_url = "https://example.com/mock-audio.mp3"
        song.save()

    def check_status(self, song):
        # Mock is always successful
        if song.generation_status != "SUCCESS":
            song.generation_status = "SUCCESS"
            song.audio_url = "https://example.com/mock-audio.mp3"
            song.save()


class SunoSongGeneratorStrategy(SongGeneratorStrategy):
    API_BASE_URL = "https://api.sunoapi.org/api/v1"
    GENERATE_ENDPOINT = f"{API_BASE_URL}/generate"
    STATUS_ENDPOINT = f"{API_BASE_URL}/generate/record-info"

    def __init__(self):
        # Get token from settings
        self.token = getattr(settings, 'SUNO_API_TOKEN', None)
        if not self.token:
            raise ValueError("SUNO_API_TOKEN not configured in settings")

    def generate_song(self, song):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        # Prepare the payload based on song fields
        payload = {
            "prompt": f"Create a song titled '{song.title}' for {song.occasion} with {song.mood_tone} mood in {song.genre} genre. Singer voice: {song.singer_voice}. Meaning: {song.meaning}",
            "duration": str(song.song_durations),  # Assuming it's in HH:MM:SS format, but API might expect seconds
            # Add other required fields as per API docs
        }

        response = requests.post(self.GENERATE_ENDPOINT, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            song.task_id = data.get('taskId')  # Assuming the response has 'taskId'
            song.generation_status = "PENDING"
            song.save()
        else:
            raise Exception(f"Failed to start generation: {response.text}")

    def check_status(self, song):
        if not song.task_id:
            return

        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        params = {
            'taskId': song.task_id
        }

        response = requests.get(self.STATUS_ENDPOINT, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            status = data.get('status')
            song.generation_status = status

            if status == "SUCCESS":
                # Assuming the response has audio_url
                song.audio_url = data.get('audio_url')  # Adjust based on actual API response

            song.save()
        else:
            raise Exception(f"Failed to check status: {response.text}")


def get_song_generator_strategy(strategy_name=None):
    """
    Factory function to get the active song generator strategy.
    
    Args:
        strategy_name: Optional strategy name ('mock' or 'suno'). 
                      If None, uses GENERATOR_STRATEGY setting.
    """
    if strategy_name is None:
        strategy_name = getattr(settings, 'GENERATOR_STRATEGY', 'mock').lower()
    else:
        strategy_name = strategy_name.lower()

    if strategy_name == 'mock':
        return MockSongGeneratorStrategy()
    elif strategy_name == 'suno':
        return SunoSongGeneratorStrategy()
    else:
        raise ValueError(f"Invalid strategy: {strategy_name}. Must be 'mock' or 'suno'.")