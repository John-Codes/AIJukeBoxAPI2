import json
import sys
import os
from LLM import LLMClient
from STT import record_audio, transcribe_audio_with_elevenlabs
from TTS import speak_text
from mongodb_handler import MongoDBHandler

class CustomSongPicker:
    def __init__(self):
        """
        Initialize the CustomSongPicker with an LLM client.
        """
        self.llm_client = LLMClient()
    
    def evaluate_song(self, song_details):
        """
        Use the LLM to evaluate a song choice based on multiple criteria and return a JSON response with:
        - boolean indicating if the song is acceptable
        - roast in ENTP dark humor raunchy style
        
        Args:
            song_details (dict): Dictionary containing song_name, genre, styles, and lyrics_description
            
        Returns:
            dict: JSON response with evaluation results
        """
        prompt = f"""
        You are an ENTP personality with dark humor and a raunchy style. Evaluate the following song choice based on all provided details:

        Song Name: "{song_details['song_name']}"
        Genre: "{song_details['genre']}"
        Musical Styles: "{song_details['styles']}"
        Lyrics Description: "{song_details['lyrics_description']}"

        Respond with a JSON object containing:
        1. "acceptable" (boolean): Whether the song is acceptable (true) or not (false)
        2. "roast" (string): A roast in ENTP dark humor raunchy style about their song choice (always include this, even for acceptable songs) and make it short and funny.

        Example format:
        {{
            "acceptable": true/false,
            "roast": "roast here"
        }}

        Be witty, playful, random funny like a ENTP comedian. Roast people in a balanced way, but keep them clever rather than just offensive. Do not use violence or drug themes. ONLY Respond in JSON no Markdown.
        """
        CleanJsonPrompt = "Please return only a valid JSON object. Do not include markdown formatting, code blocks, comments, or any extra text. The JSON must contain the following keys: acceptable (boolean) and roast (string). Ensure all quotation marks are straight quotes, and escape any special characters properly. Do not wrap the response in triple backticks or label it as JSON. Just return the raw JSON object.If the input is malformed, fix it silently and return only the corrected JSON."
        
        try:
            response = self.llm_client.call_llm(prompt)
            print("LLM Response:", response)
            # Try to parse the response as JSON
            try:
                cleanresponse =self.llm_client.call_llm(CleanJsonPrompt+response)
                print("Cleaned LLM Response:", cleanresponse)
                result = json.loads(cleanresponse)
                # Ensure all required keys are present
                if all(key in result for key in ["acceptable", "roast"]):
                    return result
                else:
                    # If JSON doesn't have required structure, create a default response
                    return {
                        "acceptable": False,
                        "roast": "Even your song choice is basic. Try again, normie."
                    }
            except json.JSONDecodeError:
                # If response isn't valid JSON, create a default response
                return {
                    "acceptable": False,
                    "roast": f"Is '{song_details['song_name']}' supposed to be music or just noise? Try again."
                }
        except Exception as e:
            # Handle any other errors
            return {
                "acceptable": False,
                "roast": f"Nice try, but I can't even process your song choice: {str(e)}"
            }
    
    def collect_song_details(self):
        """
        Collect detailed song information from the user.
        
        Returns:
            dict: Dictionary containing song_name, genre, styles, and lyrics_description
        """
        print("Please provide details about your song choice.")
        speak_text("Please provide details about your song choice.")
        
        # Collect song name
        print("\nWhat's the name of your song?")
        speak_text("What's the name of your song?")
        audio_filename = record_audio(record_seconds=5)
        transcription = transcribe_audio_with_elevenlabs(audio_filename)
        song_name = transcription.text.strip()
        print(f"Song name: {song_name}")
        
        if song_name.lower() == 'quit':
            print("Giving up already? Typical.")
            speak_text("Giving up already? Typical.")
            sys.exit(0)
        
        if not song_name:
            print("Silence isn't a song, genius. Let's try again.")
            speak_text("Silence isn't a song, genius. Let's try again.")
            return None
        
        # Collect genre
        print("\nWhat's the genre of your song?")
        speak_text("What's the genre of your song?")
        audio_filename = record_audio(record_seconds=5)
        transcription = transcribe_audio_with_elevenlabs(audio_filename)
        genre = transcription.text.strip()
        print(f"Genre: {genre}")
        
        if genre.lower() == 'quit':
            print("Giving up already? Typical.")
            speak_text("Giving up already? Typical.")
            sys.exit(0)
        
        # Collect musical styles
        print("\nDescribe the musical styles of your song.")
        speak_text("Describe the musical styles of your song.")
        audio_filename = record_audio(record_seconds=7)
        transcription = transcribe_audio_with_elevenlabs(audio_filename)
        styles = transcription.text.strip()
        print(f"Musical styles: {styles}")
        
        if styles.lower() == 'quit':
            print("Giving up already? Typical.")
            speak_text("Giving up already? Typical.")
            sys.exit(0)
        
        # Collect lyrics description
        print("\nDescribe the lyrics of your song.")
        speak_text("Describe the lyrics of your song.")
        audio_filename = record_audio(record_seconds=10)
        transcription = transcribe_audio_with_elevenlabs(audio_filename)
        lyrics_description = transcription.text.strip()
        print(f"Lyrics description: {lyrics_description}")
        
        if lyrics_description.lower() == 'quit':
            print("Giving up already? Typical.")
            speak_text("Giving up already? Typical.")
            sys.exit(0)
        
        return {
            "song_name": song_name,
            "genre": genre,
            "styles": styles,
            "lyrics_description": lyrics_description
        }
    
    def pick_song(self):
        """
        Main method to run the song picking loop with detailed user input.
        
        Returns:
            dict: Final JSON response when an acceptable song is selected
        """
        print("Welcome to the AI Jukebox! Pick a song and prepare to be roasted!")
        speak_text("Welcome to the AI Jukebox! Pick a song and prepare to be roasted!")
        
        while True:
            song_details = self.collect_song_details()
            
            if song_details is None:
                continue
            
            # Evaluate the song choice
            result = self.evaluate_song(song_details)
            
            # Display the roast regardless of acceptability
            print(f"\nRoast: {result['roast']}")
            speak_text(result['roast'])
            
            # Check if the song is acceptable
            if result['acceptable']:
                print("\nFinally! You picked an acceptable song.")
                speak_text("Finally! You picked an acceptable song.")
                return result, song_details
            else:
                print("Try again, oh master of terrible music choices.")
                speak_text("Try again, oh master of terrible music choices.")

if __name__ == "__main__":
    # Create an instance of CustomSongPicker and run it
    song_picker = CustomSongPicker()
    final_result, song_details = song_picker.pick_song()
    print(f"\nYou picked: {song_details['song_name']}")
    print(f"Genre: {song_details['genre']}")
    print(f"Styles: {song_details['styles']}")
    print(f"Lyrics: {song_details['lyrics_description']}")
    
    print("\nFinal result:")
    print(json.dumps(final_result, indent=2))
    
    # Save to MongoDB
    try:
        mongo_handler = MongoDBHandler()
        song_data = {
            "song_name": song_details['song_name'],
            "genre": song_details['genre'],
            "styles": song_details['styles'],
            "lyrics_description": song_details['lyrics_description'],
            "acceptable": final_result['acceptable'],
            "roast": final_result['roast']
        }
        success = mongo_handler.insert_song_data(song_data)
        if success:
            print("\nSong data successfully saved to MongoDB!")
        else:
            print("\nFailed to save song data to MongoDB.")
        mongo_handler.close_connection()
    except Exception as e:
        print(f"\nError saving to MongoDB: {e}")
