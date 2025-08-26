import time
import random
from LLM import LLMClient
from TTS import speak_text
from STT import record_audio, transcribe_audio_with_elevenlabs
from songpicker import SongPicker
from custom_songpicker import CustomSongPicker
import re

from colorama import init, Fore, Style
init(autoreset=True)  # Initialize colorama


# Define color constants
LISTEN_COLOR = Fore.LIGHTBLUE_EX
API_COLOR = Fore.YELLOW
JOKE_COLOR = Fore.MAGENTA
SONG_COLOR = Fore.GREEN
CUSTOM_SONG_COLOR = Fore.CYAN
RESET_COLOR = Style.RESET_ALL

class JukeboxJokeTeller:
    def __init__(self):
        """
        Initialize the JukeboxJokeTeller with an LLM client and song pickers.
        """
        self.llm_client = LLMClient()
        self.song_picker = SongPicker()
        self.custom_song_picker = CustomSongPicker()
        self.joke_count = 0
        self.offer_frequency = 3  # Make an offer every 3 jokes
    
    def _parse_json_response(self, response_text, clean_prompt=None):
        """
        Helper method to parse JSON response with optional cleaning.
        
        Args:
            response_text (str): The response text to parse
            clean_prompt (str, optional): Prompt to clean the response if needed
            
        Returns:
            dict: Parsed JSON result or None if parsing fails
        """
        import json
        try:
            # Remove Markdown formatting
            cleaned_response = re.sub(r"```json|```", "", response_text).strip()
            
            # Try to parse the response as JSON
            result = json.loads(cleaned_response)
            
            # Ensure all required keys are present
            if all(key in result for key in ["relevant", "type", "confidence"]):
                return result
        except:
            pass  # Continue to cleaning attempt if provided
        
        # If parsing failed and we have a clean prompt, try cleaning
        if clean_prompt:
            try:
                clean_response = self.llm_client.call_llm(clean_prompt + response_text)
                print(Fore.YELLOW + "Cleaned JSON response:" + Style.RESET_ALL, clean_response)
                
                result = json.loads(clean_response)
                if all(key in result for key in ["relevant", "type", "confidence"]):
                    return result
            except:
                pass  # Will return None to indicate failure
        
        return None  # Indicates parsing failed
    
    def validate_user_request(self, user_input):
        """
        Use the LLM to validate if user input relates to the song offer.
        
        Args:
            user_input (str): The user's spoken input
            
        Returns:
            dict: JSON response with validation results
        """
        prompt = f"""
        You are evaluating user input to determine if they want songs or custom songs based on our offer.
        Our offer is: "I can play songs for you or make a song for your loved ones or yourself for just $1 USD each."
        
        User said: "{user_input}"
        
        Respond with a JSON object containing:
        1. "relevant" (boolean): Whether the user's input relates to our song offer
        2. "type" (string): Either "play" for playing existing songs, "custom" for custom songs, or "none" if not relevant
        3. "confidence" (string): How confident you are in your assessment ("high", "medium", "low")
        
        Example format:
        {{
            "relevant": true/false,
            "type": "play/custom/none",
            "confidence": "high/medium/low"
        }}
        
        ONLY Respond in JSON no Markdown.
        """
        CleanJsonPrompt = "Please return only a valid JSON object. Do not include markdown formatting, code blocks, comments, or any extra text. The JSON must contain the following keys: relevant (boolean), type (string), and confidence (string). Ensure all quotation marks are straight quotes, and escape any special characters properly. Do not wrap the response in triple backticks or label it as JSON. Just return the raw JSON object. If the input is malformed, fix it silently and return only the corrected JSON."
        
        try:
            print(f"{API_COLOR}Calling LLM for user request validation...{RESET_COLOR}")
            response = self.llm_client.call_llm(prompt)
            print(Fore.CYAN + "LLM Response:" + Style.RESET_ALL, response)

            # Try to parse the response
            result = self._parse_json_response(response, CleanJsonPrompt)
            
            # Return parsed result or default response
            return result if result else {
                "relevant": False,
                "type": "none",
                "confidence": "low"
            }
        except Exception as e:
            print(f"Error validating user request: {e}")
            return {
                "relevant": False,
                "type": "none",
                "confidence": "low"
            }
    
    def listen_once(self):
        """
        Listen for user input once (blocking call).
        Returns True if user input was processed, False otherwise.
        """
        try:
            # Record audio from microphone (5 seconds)
            print(f"{LISTEN_COLOR}Listening for user input...{RESET_COLOR}")
            audio_filename = record_audio(record_seconds=5)
            
            # Transcribe using ElevenLabs
            transcription = transcribe_audio_with_elevenlabs(audio_filename)
            user_input = transcription.text.strip()
            
            if user_input:
                print(f"{LISTEN_COLOR}User said: {user_input}{RESET_COLOR}")
                
                # Validate if user input relates to our offer
                validation = self.validate_user_request(user_input)
                print(f"{LISTEN_COLOR}Validation result: {validation}{RESET_COLOR}")
                
                if validation["relevant"] and validation["confidence"] in ["high", "medium"]:
                    if validation["type"] == "play":
                        speak_text("Great! Let's pick a song for you.")
                        print(f"{SONG_COLOR}Going to song picker...{RESET_COLOR}")
                        self.song_picker.pick_song()
                    elif validation["type"] == "custom":
                        speak_text("Awesome! Let's create a custom song for you.")
                        print(f"{CUSTOM_SONG_COLOR}Going to custom song picker...{RESET_COLOR}")
                        self.custom_song_picker.pick_song()
                return True
            return False
        except Exception as e:
            print(f"Error in listening: {e}")
        return False
    
    def tell_joke(self):
        """
        Use the LLM to generate an ENTP-style joke with dark humor and social critiques.
        
        Returns:
            str: The generated joke
        """
        prompt = """
        You are an ENTP personality with dark humor who loves to roast society, unfair jobs, and life situations.
        Tell a short, witty joke that:
        1. Critiques society, corporate culture, expensive rent, expensive mortgages, or unfair life situations
        2. Has ENTP-style dark humor (clever, not mean-spirited)
        3. Is concise and funny
        4. Roasts the absurdity of modern life, work, or social expectations
        
       
        Generate an original joke following this style:
        """
        
        try:
            print(f"{API_COLOR}Calling LLM for joke generation...{RESET_COLOR}")
            joke = self.llm_client.call_llm(prompt)
            print(f"{JOKE_COLOR}Joke: {joke.strip()}{RESET_COLOR}")
            return joke.strip()
        except Exception as e:
            error_message = "Uh oh, I couldn't come up with a joke right now. Even my creativity is on strike!"
            print(f"Error generating joke: {e}")
            return error_message
    
    def offer(self):
        """
        Make an offer to play songs or make custom songs.
        """
        offer_text = "I can play songs for you or make a song for your loved ones or yourself for just $1 each."
        speak_text(offer_text)
        print(f"Offer: {offer_text}")
    
    def run(self):
        """
        Main loop that alternates between listening and telling jokes in the same thread.
        """
        print("Jukebox Joke Teller started! Enjoy the humor...")
        speak_text("Welcome to the crooked Jukebox! Prepare for some crazy shit!")
        
        # Initial offer
        self.offer()
        
        # Main loop that alternates between listening and joke telling
        while True:
            try:
                # Listen for user input
                user_input_processed = self.listen_once()
                
               
                # # If user input was processed, continue to next iteration
                # if user_input_processed:
                #     continue

                # Tell a joke
                joke = self.tell_joke()
                print(f"Joke: {joke}")
                speak_text(joke)


                # Wait a few seconds for the joke audio to finish playing
                time.sleep(5)


                # Increment joke counter
                self.joke_count += 1
                
                # Make an offer every few jokes
                if self.joke_count % self.offer_frequency == 0:
                    time.sleep(2)  # Brief pause before offer
                    self.offer()
                    time.sleep(3)  # Wait for offer to finish playing
                
                # Wait before next cycle (random interval for natural feel)
                wait_time = random.randint(8, 15)
                time.sleep(wait_time)
                 # If user input was processed, continue to next iteration
                if user_input_processed:
                    continue
            except Exception as e:
                print(f"Error in main loop: {e}")
                speak_text("Oops, something went wrong with the joke loop. Let me try to recover...")
                time.sleep(5)  # Wait before continuing

if __name__ == "__main__":
    # Create an instance of JukeboxJokeTeller and run it
    joke_teller = JukeboxJokeTeller()
    try:
        joke_teller.run()
    except KeyboardInterrupt:
        print("\nJukebox Joke Teller stopped.")
        speak_text("Thanks for listening! Come back anytime for more social commentary!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        speak_text("Uh oh, something went wrong. But hey, that's just like life - full of unexpected errors!")
