# pip install pocketsphinx
# pip install pyaudio
# do this on crusty old work station (18.04, really need to upgrade this box :P) 
# pip install pocketsphinx==5.0.2

import os
import pyaudio
from pocketsphinx import LiveSpeech

def speech_to_text() -> None:
    """
    Opens the microphone, captures audio in real-time, and prints the transcribed text.
    This function uses PocketSphinx for speech recognition and runs indefinitely.

    Input parameters: None
    """

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Audio stream parameters
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)

    # Configure PocketSphinx for live speech recognition
    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=os.path.join('model/sphinx/', 'en-us'),  # Path to the acoustic model
        lm=os.path.join('model/sphinx/', 'en-us.lm.bin'),  # Path to the language model
        dic=os.path.join('model/sphinx/', 'cmudict-en-us.dict')  # Path to the phonetic dictionary
    )

    print("Speech to Text started. Speak into the microphone.")
    try:
        # Process audio chunks from the microphone input
        for phrase in speech:
            print(phrase)
    except KeyboardInterrupt:
        # Handle exit gracefully
        print("\nExiting Speech to Text...")
    finally:
        # Clean up PyAudio stream
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    speech_to_text()