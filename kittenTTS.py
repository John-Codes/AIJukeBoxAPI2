from kittentts import KittenTTS
from huggingface_hub import login
import os
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HUGGINGFACE_TOKEN")
if hf_token:
    login(hf_token)
else:
    raise ValueError("HUGGINGFACE_TOKEN not found in environment variables")

m = KittenTTS("KittenML/kitten-tts-nano-0.2")

audio = m.generate("welcome to the crooked Jukebox! prepare for some crazy shit! .", voice='expr-voice-3-f' )
#expr-voice-3-f

# available_voices : [  'expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f',  'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f' ]

# Save the audio
import soundfile as sf
sf.write('output.wav', audio, 24000)
