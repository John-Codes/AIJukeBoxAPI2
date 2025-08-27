class Status:
    """
    A class to manage the status of song loading and playing.
    This follows the Single Responsibility Principle by focusing only on status management.
    """
    
    def __init__(self):
        """
        Initialize the status flags.
        """
        self._loading_song = False
        self._playing_song = False
        self._loading_custom_song = False
        self._playing_custom_song = False
    
    @property
    def loading_song(self):
        """
        Get the loading_song status.
        
        Returns:
            bool: True if a song is currently loading, False otherwise.
        """
        return self._loading_song
    
    @loading_song.setter
    def loading_song(self, value):
        """
        Set the loading_song status.
        
        Args:
            value (bool): The new loading status.
        """
        self._loading_song = bool(value)
    
    @property
    def playing_song(self):
        """
        Get the playing_song status.
        
        Returns:
            bool: True if a song is currently playing, False otherwise.
        """
        return self._playing_song
    
    @playing_song.setter
    def playing_song(self, value):
        """
        Set the playing_song status.
        
        Args:
            value (bool): The new playing status.
        """
        self._playing_song = bool(value)
    
    @property
    def loading_custom_song(self):
        """
        Get the loading_custom_song status.
        
        Returns:
            bool: True if a custom song is currently loading, False otherwise.
        """
        return self._loading_custom_song
    
    @loading_custom_song.setter
    def loading_custom_song(self, value):
        """
        Set the loading_custom_song status.
        
        Args:
            value (bool): The new loading status for custom songs.
        """
        self._loading_custom_song = bool(value)
    
    @property
    def playing_custom_song(self):
        """
        Get the playing_custom_song status.
        
        Returns:
            bool: True if a custom song is currently playing, False otherwise.
        """
        return self._playing_custom_song
    
    @playing_custom_song.setter
    def playing_custom_song(self, value):
        """
        Set the playing_custom_song status.
        
        Args:
            value (bool): The new playing status for custom songs.
        """
        self._playing_custom_song = bool(value)
    
    def is_song_active(self):
        """
        Check if any song activity is happening (loading or playing).
        
        Returns:
            bool: True if a song is loading or playing, False otherwise.
        """
        return self._loading_song or self._playing_song or self._loading_custom_song or self._playing_custom_song
