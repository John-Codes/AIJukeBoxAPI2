import os
import pyaudio
import wave
from dotenv import load_dotenv
from io import BytesIO
import requests
from elevenlabs.client import ElevenLabs

load_dotenv()

elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def record_audio(filename="recorded_audio.wav", record_seconds=5):
    """
    Record audio from microphone and save to WAV file
    """
    # Audio parameters
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    sample_rate = 44100
    
    p = pyaudio.PyAudio()
    
    print("Recording...")
    
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=sample_rate,
                    frames_per_buffer=chunk,
                    input=True)
    
    frames = []
    
    # Record for the specified number of seconds
    for i in range(0, int(sample_rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    print("Finished recording")
    
    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return filename

def transcribe_audio_with_elevenlabs(audio_filename):
    """
    Transcribe audio using ElevenLabs API
    """
    # Read the audio file
    with open(audio_filename, "rb") as audio_file:
        audio_data = BytesIO(audio_file.read())
    
    # Send to ElevenLabs for transcription
    transcription = elevenlabs.speech_to_text.convert(
        file=audio_data,
        model_id="scribe_v1",  # Model to use, for now only "scribe_v1" is supported
        tag_audio_events=True,  # Tag audio events like laughter, applause, etc.
        language_code="eng",  # Language of the audio file
        diarize=True,  # Whether to annotate who is speaking
    )
    
    return transcription

if __name__ == "__main__":
    # Record audio from microphone (5 seconds)
    audio_filename = record_audio(record_seconds=5)
    
    # Transcribe using ElevenLabs
    transcription = transcribe_audio_with_elevenlabs(audio_filename)
    
    print("Transcription:")
    print(transcription.text)