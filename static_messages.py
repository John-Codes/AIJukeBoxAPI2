import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import soundfile as sf
import numpy as np

# Load environment variables
load_dotenv()

class StaticMessages:
    def __init__(self, audio_dir="static_audio"):
        """
        Initialize the StaticMessages class.
        
        Args:
            audio_dir (str): Directory to store static audio files
        """
        self.audio_dir = audio_dir
        self.elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        
        # Create audio directory if it doesn't exist
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)
    
    def create_static_message(self, text, message_id, voice_id="JBFqnCBsd6RMkjVDRZzb", model_id="eleven_multilingual_v2"):
        """
        Generate and save a static message as an audio file.
        
        Args:
            text (str): The text to convert to speech
            message_id (str): Unique identifier for the message
            voice_id (str): The voice ID to use
            model_id (str): The model ID to use
            
        Returns:
            str: Path to the saved audio file
        """
        try:
            # Generate audio using ElevenLabs
            audio = self.elevenlabs.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id=model_id,
                output_format="mp3_44100_128",
            )
            
            # Save audio file
            file_path = os.path.join(self.audio_dir, f"{message_id}.mp3")
            
            # Write audio data to file
            with open(file_path, "wb") as f:
                for chunk in audio:
                    f.write(chunk)
            
            print(f"Static message '{message_id}' created and saved to {file_path}")
            return file_path
        except Exception as e:
            print(f"Error creating static message '{message_id}': {e}")
            return None
    
    def play_static_message(self, message_id):
        """
        Play a pre-recorded static message.
        
        Args:
            message_id (str): Unique identifier for the message
            
        Returns:
            bool: True if message was played successfully, False otherwise
        """
        try:
            from elevenlabs import play
            
            file_path = os.path.join(self.audio_dir, f"{message_id}.mp3")
            
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"Static message '{message_id}' not found at {file_path}")
                return False
            
            # Play the audio file
            with open(file_path, "rb") as audio_file:
                play(audio_file.read())
            
            return True
        except Exception as e:
            print(f"Error playing static message '{message_id}': {e}")
            return False
    
    def get_message_text(self, message_id):
        """
        Get the text of a static message from a text file.
        
        Args:
            message_id (str): Unique identifier for the message
            
        Returns:
            str: The text of the message or None if not found
        """
        try:
            text_file_path = os.path.join(self.audio_dir, f"{message_id}.txt")
            if os.path.exists(text_file_path):
                with open(text_file_path, "r") as f:
                    return f.read().strip()
            return None
        except Exception as e:
            print(f"Error reading text for message '{message_id}': {e}")
            return None

def main():
    """
    Test function to create and play static messages.
    """
    # Initialize StaticMessages
    static_msgs = StaticMessages()
    
    # Example static messages that could be used in the jukebox
    messages = {
        "welcome": "Welcome to the crooked Jukebox! Prepare for some crazy shit!",
        "song_choice_prompt": "Please say your song choice...",
        "custom_song_prompt": "Please provide details about your song choice.",
        "song_name_prompt": "What's the name of your song?",
        "genre_prompt": "What's the genre of your song?",
        "styles_prompt": "Describe the musical styles of your song.",
        "lyrics_prompt": "Describe the lyrics of your song.",
        "roast_intro": "Prepare to be roasted!",
        "try_again": "Try again, oh master of terrible music choices.",
        "acceptable_song": "Finally! You picked an acceptable song.",
        "confirm_prompt": "Do you confirm this song choice?",
        "song_confirmed": "Song confirmed! Enjoy your music.",
        "offer": "I can play songs for you or make a song for your loved ones or yourself for just $1 each.",
        "pick_song": "Great! Let's pick a song for you.",
        "create_custom_song": "Awesome! Let's create a custom song for you.",
        "song_selection_cancelled": "Song selection was cancelled. Let's continue with the jokes.",
        "song_selected_confirmed": "Your song has been selected and confirmed. Enjoy!",
        "custom_song_selection_cancelled": "Song selection was cancelled. Let's continue with the jokes.",
        "custom_song_selected_confirmed": "Your custom song has been selected and confirmed. Enjoy!",
        "giving_up": "Giving up already? Typical.",
        "silence_not_song": "Silence isn't a song, genius. Try again.",
        "silence_not_song_custom": "Silence isn't a song, genius. Let's try again.",
        "song_confirmed_enjoy": "Song confirmed! Enjoy your music.",
        "pick_different_song": "Let's pick a different song.",
        "pick_different_song_custom": "Let's choose a different song.",
        "song_selection_cancelled_custom": "Song selection cancelled.",
        "confirmation_low_confidence": "I didn't catch that. Please say yes to confirm, no to choose a different song, or cancel to exit.",
        "confirmation_no_input": "I didn't hear anything. Please say yes to confirm, no to choose a different song, or cancel to exit.",
        "confirmation_error": "There was an error processing your response. Please try again."
    }
    
    print("Creating and testing all static messages...")
    print("=" * 50)
    
    # Create and test each message
    for msg_id, text in messages.items():
        print(f"\n--- Testing message: {msg_id} ---")
        print(f"Text: {text}")
        
        # Save the text for reference
        text_file_path = os.path.join(static_msgs.audio_dir, f"{msg_id}.txt")
        with open(text_file_path, "w") as f:
            f.write(text)
        
        # Check if audio file already exists
        audio_file_path = os.path.join(static_msgs.audio_dir, f"{msg_id}.mp3")
        if os.path.exists(audio_file_path):
            print(f"Audio file for '{msg_id}' already exists")
        else:
            # Create the audio file
            file_path = static_msgs.create_static_message(text, msg_id)
            if file_path:
                print(f"Successfully created audio for '{msg_id}'")
            else:
                print(f"Failed to create audio for '{msg_id}'")
                continue
        
        # Play the message
        print(f"Playing '{msg_id}' message...")
        static_msgs.play_static_message(msg_id)
        import time
        time.sleep(2)  # Wait for playback to finish
        
        print(f"Completed testing for '{msg_id}'")
    
    print("\n" + "=" * 50)
    print("All static messages have been created and tested!")
    print("To play any message, use: static_msgs.play_static_message('message_id')")
    print("Available message IDs:", list(messages.keys()))

if __name__ == "__main__":
    main()
