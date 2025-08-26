from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os

load_dotenv()

# Initialize ElevenLabs client
elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def speak_text(text, voice_id="JBFqnCBsd6RMkjVDRZzb", model_id="eleven_multilingual_v2"):
    """
    Convert text to speech and play it using ElevenLabs API.
    
    Args:
        text (str): The text to convert to speech
        voice_id (str): The voice ID to use (default: JBFqnCBsd6RMkjVDRZzb)
        model_id (str): The model ID to use (default: eleven_multilingual_v2)
    """
    try:
        audio = elevenlabs.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            output_format="mp3_44100_128",
        )
        play(audio)
    except Exception as e:
        print(f"Error in TTS: {e}")

if __name__ == "__main__":
    # Example usage
    speak_text("Hi I make custom songs in minutes for fun or for special ocasions")
