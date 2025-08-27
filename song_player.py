import threading
import time
import pygame
import os
from status import Status

class SongPlayer:
    """
    A class to handle playing songs and managing the status during playback.
    This follows the Single Responsibility Principle by focusing only on song playing.
    """
    
    def __init__(self, status: Status):
        """
        Initialize the SongPlayer with a Status instance.
        
        Args:
            status (Status): The status instance to manage during song playback.
        """
        self.status = status
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
    
    def play_song(self, song_name="DemoSong.wav"):
        """
        Play a song and manage the status flags during playback.
        This method will block until the song finishes playing.
        
        Args:
            song_name (str): Name of the song to play. Defaults to "DemoSong.wav".
        """
        # Clean up the song name by removing trailing punctuation
        cleaned_song_name = song_name.rstrip('. ')
        song_path = f"{cleaned_song_name}.wav"
        
        # If the cleaned song file doesn't exist, use the demo song as fallback
        if not os.path.exists(song_path):
            song_path = "DemoSong.wav"
            print(f"Song '{cleaned_song_name}' not found, using demo song instead.")
        
        # Set loading status
        self.status.loading_song = True
        print(f"Loading song: {song_path}")
        
        try:
            # Load the song
            pygame.mixer.music.load(song_path)
            
            # Set playing status and clear loading status
            self.status.loading_song = False
            self.status.playing_song = True
            print(f"Playing song: {song_path}")
            
            # Start playback
            pygame.mixer.music.play()
            
            # Wait until the song finishes playing
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Clear playing status when finished
            self.status.playing_song = False
            print(f"Finished playing song: {song_path}")
            
        except Exception as e:
            print(f"Error playing song: {e}")
            # Clear both status flags in case of error
            self.status.loading_song = False
            self.status.playing_song = False
    
    def play_song_async(self, song_path="DemoSong.wav"):
        """
        Play a song asynchronously without blocking the calling thread.
        This method returns immediately after starting playback.
        
        Args:
            song_path (str): Path to the song file to play. Defaults to "DemoSong.wav".
        """
        # Create and start a new thread for song playback
        playback_thread = threading.Thread(target=self.play_song, args=(song_path,))
        playback_thread.daemon = True  # Thread will die when main program exits
        playback_thread.start()
    
    def play_custom_song(self, song_details):
        """
        Play a custom song and manage the status flags during playback.
        This method will block until the song finishes playing.
        
        Args:
            song_details (dict): Dictionary containing details about the custom song.
        """
        # Set loading status for custom song
        self.status.loading_custom_song = True
        print(f"Loading custom song: {song_details.get('song_name', 'Unknown')}")
        
        try:
            # For now, we'll play the demo song as a placeholder
            # In a real implementation, this would generate and play the custom song
            song_path = "DemoSong.wav"
            
            # Load the song
            pygame.mixer.music.load(song_path)
            
            # Set playing status and clear loading status
            self.status.loading_custom_song = False
            self.status.playing_custom_song = True
            print(f"Playing custom song: {song_details.get('song_name', 'Unknown')}")
            
            # Start playback
            pygame.mixer.music.play()
            
            # Wait until the song finishes playing
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Clear playing status when finished
            self.status.playing_custom_song = False
            print(f"Finished playing custom song: {song_details.get('song_name', 'Unknown')}")
            
        except Exception as e:
            print(f"Error playing custom song: {e}")
            # Clear both status flags in case of error
            self.status.loading_custom_song = False
            self.status.playing_custom_song = False
