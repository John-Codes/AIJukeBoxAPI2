import sys
from LLM import LLMClient
from STT import record_audio, transcribe_audio_with_elevenlabs
from TTS import speak_text
from static_messages import StaticMessages
from json_parser import JSONResponseParser

class Confirmation:
    def __init__(self):
        """
        Initialize the Confirmation class with necessary components.
        """
        self.llm_client = LLMClient()
        self.json_parser = JSONResponseParser(self.llm_client)
        self.static_msgs = StaticMessages()
    
    def validate_confirmation(self, user_input):
        """
        Use the LLM to validate if user input relates to confirming or changing their song choice.
        
        Args:
            user_input (str): The user's spoken input
            
        Returns:
            dict: JSON response with validation results
        """
        prompt = f"""
        You are evaluating user input to determine if they want to confirm their song choice or select a different song.
        
        User said: "{user_input}"
        
        Respond with a JSON object containing:
        1. "confirmed" (boolean): Whether the user wants to confirm their song choice
        2. "change_song" (boolean): Whether the user wants to select a different song
        3. "cancel" (boolean): Whether the user wants to cancel the song selection
        4. "confidence" (string): How confident you are in your assessment ("high", "medium", "low")
        
        Example format:
        {{
            "confirmed": true/false,
            "change_song": true/false,
            "cancel": true/false,
            "confidence": "high/medium/low"
        }}
        
        ONLY Respond in JSON no Markdown.
        """
        CleanJsonPrompt = "Please return only a valid JSON object. Do not include markdown formatting, code blocks, comments, or any extra text. The JSON must contain the following keys: confirmed (boolean), change_song (boolean), cancel (boolean), and confidence (string). Ensure all quotation marks are straight quotes, and escape any special characters properly. Do not wrap the response in triple backticks or label it as JSON. Just return the raw JSON object. If the input is malformed, fix it silently and return only the corrected JSON."
        
        try:
            print(f"Calling LLM for confirmation validation...")
            response = self.llm_client.call_llm(prompt)
            print(f"LLM Response: {response}")

            # Try to parse the response
            result = self.json_parser.parse_confirmation_json(response, CleanJsonPrompt)
            
            # Return parsed result or default response
            return result if result else {
                "confirmed": False,
                "change_song": False,
                "cancel": True,
                "confidence": "low"
            }
        except Exception as e:
            print(f"Error validating confirmation: {e}")
            return {
                "confirmed": False,
                "change_song": False,
                "cancel": True,
                "confidence": "low"
            }
    
    def confirm_song_choice(self, song_choice):
        """
        Ask the user to confirm their song choice.
        
        Args:
            song_choice (str or dict): The user's song choice (string for simple songs, dict for custom songs)
            
        Returns:
            str: Action to take ("confirmed", "change_song", "cancel")
        """
        # Create the confirmation message based on song type
        if isinstance(song_choice, dict):
            # Custom song with multiple details
            confirmation_message = f"Are you sure you want to proceed with {song_choice.get('song_name', 'your song')} in the {song_choice.get('genre', 'specified')} genre?"
        else:
            # Simple song choice
            confirmation_message = f"Are you sure you want to proceed with {song_choice}?"
        
        print(f"Confirmation: {confirmation_message}")
        
        # Play static confirmation message
        self.static_msgs.play_static_message("confirm_prompt")
        
        while True:
            try:
                # Record audio from microphone (5 seconds)
                print("Listening for your confirmation...")
                audio_filename = record_audio(record_seconds=5)
                
                # Transcribe using ElevenLabs
                transcription = transcribe_audio_with_elevenlabs(audio_filename)
                user_input = transcription.text.strip()
                
                if user_input:
                    print(f"User said: {user_input}")
                    
                    # Validate user input
                    validation = self.validate_confirmation(user_input)
                    print(f"Validation result: {validation}")
                    
                    if validation["confidence"] in ["high", "medium"]:
                        if validation["confirmed"]:
                            return "confirmed"
                        elif validation["change_song"]:
                            return "change_song"
                        elif validation["cancel"]:
                            return "cancel"
                    else:
                        # Low confidence, ask user to repeat
                        self.static_msgs.play_static_message("confirmation_low_confidence")
                        self.static_msgs.play_static_message("try_again")
                else:
                    # No input, ask user to repeat
                    self.static_msgs.play_static_message("confirmation_no_input")
                    self.static_msgs.play_static_message("try_again")
            except Exception as e:
                print(f"Error in confirmation: {e}")
                self.static_msgs.play_static_message("confirmation_error")
                self.static_msgs.play_static_message("try_again")
