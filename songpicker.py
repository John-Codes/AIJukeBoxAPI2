import sys
import os
import json
from LLM import LLMClient
from STT import record_audio, transcribe_audio_with_elevenlabs
from TTS import speak_text
from mongodb_handler import MongoDBHandler
from json_parser import JSONResponseParser
from static_messages import StaticMessages
from confirmation import Confirmation

class SongPicker:
    def __init__(self):
        """
        Initialize the SongPicker with an LLM client.
        """
        self.llm_client = LLMClient()
        self.json_parser = JSONResponseParser(self.llm_client)
        self.static_msgs = StaticMessages()
    
    def evaluate_song(self, song_choice):
        """
        Use the LLM to evaluate a song choice and return a JSON response with:
        - boolean indicating if the song is acceptable
        - description of the user's song choice
        - roast in ENTP dark humor raunchy style
        
        Args:
            song_choice (str): The user's song selection
            
        Returns:
            dict: JSON response with evaluation results
        """
        prompt = f"""
        You are an ENTP personality with dark humor and a raunchy style. Evaluate the following song choice:

        Song: "{song_choice}"

        Respond with a JSON object containing:
        1. "acceptable" (boolean): Whether the song is acceptable (true) or not (false)
        2. "roast" (string): A roast in ENTP dark humor raunchy style about their song choice (always include this, even for acceptable songs) and make it short and funny.

        Example format:
        {{
            "acceptable": true/false,
            "roast": "roast here"
        }}

        Be witty, playful,random funny like a ENTP comedian. Roast people in a balanced way, but keep them clever rather than just offensive. Do not use violence or drug themes. ONLY Respond in JSON no Markdown.
        """
        CleanJsonPrompt = "Please return only a valid JSON object. Do not include markdown formatting, code blocks, comments, or any extra text. The JSON must contain the following keys: acceptable (boolean) and roast (string). Ensure all quotation marks are straight quotes, and escape any special characters properly. Do not wrap the response in triple backticks or label it as JSON. Just return the raw JSON object.If the input is malformed, fix it silently and return only the corrected JSON."
        
        try:
            response = self.llm_client.call_llm(prompt)
            print("LLM Response:", response)
            
            # Use JSONResponseParser to parse the response
            result = self.json_parser.parse_song_picker_json(response, CleanJsonPrompt)
            
            # Return parsed result or default response
            return result if result else {
                "acceptable": False,
                "roast": "Even your song choice is basic. Try again, normie."
            }
        except Exception as e:
            # Handle any other errors
            return {
                "acceptable": False,
                "roast": f"Nice try, but I can't even process your song choice: {str(e)}"
            }
    
    def pick_song(self):
        """
        Main method to run the song picking loop with user input.
        
        Returns:
            dict: Final JSON response when an acceptable song is selected
        """
        self.static_msgs.play_static_message("roast_intro")
        
        while True:
            print("\nPlease say your song choice...")
            self.static_msgs.play_static_message("song_choice_prompt")
            
            # Record audio from microphone (5 seconds)
            audio_filename = record_audio(record_seconds=5)
            
            # Transcribe using ElevenLabs
            transcription = transcribe_audio_with_elevenlabs(audio_filename)
            song_choice = transcription.text.strip()
            
            print(f"You said: {song_choice}")
            
            if song_choice.lower() == 'quit':
                self.static_msgs.play_static_message("giving_up")
                self.static_msgs.play_static_message("try_again")
                sys.exit(0)
            
            if not song_choice:
                self.static_msgs.play_static_message("silence_not_song")
                self.static_msgs.play_static_message("try_again")
                continue
            
            # Evaluate the song choice
            result = self.evaluate_song(song_choice)
            
            # Display the roast regardless of acceptability
            print(f"\nRoast: {result['roast']}")
            speak_text(result['roast'])
            
           
            
            # Check if the song is acceptable
            if result['acceptable']:
                print("\nFinally! You picked an acceptable song.")
                self.static_msgs.play_static_message("acceptable_song")
                
                # Ask for confirmation
                confirmation = Confirmation()
                action = confirmation.confirm_song_choice(song_choice)
                
                if action == "confirmed":
                    print("Song confirmed!")
                    return result, song_choice
                elif action == "change_song":
                    print("Let's pick a different song.")
                    self.static_msgs.play_static_message("try_again")
                    continue
                elif action == "cancel":
                    print("Song selection cancelled.")
                    self.static_msgs.play_static_message("try_again")
                    return None, None
            else:
                print("Try again, oh master of terrible music choices.")
                self.static_msgs.play_static_message("try_again")

if __name__ == "__main__":
    # Create an instance of SongPicker and run it
    song_picker = SongPicker()
    final_result, song_choice = song_picker.pick_song()
    print(f"You picked: {song_choice}")
    
    print("\nFinal result:")
    print(json.dumps(final_result, indent=2))
    
    # Save to MongoDB
    try:
        mongo_handler = MongoDBHandler()
        song_data = {
            "song_name": song_choice,
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
