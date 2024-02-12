from vosk import Model, KaldiRecognizer
import os
import pyaudio

def continuous_speech_to_text() -> None:
    """
    Captures audio from the microphone, performs speech-to-text using Vosk, and prints the text continuously.

    Input parameters: None
    """

    # Load the Vosk model
    model_path = "model"  # Adjust the path to your Vosk model directory
    if not os.path.exists(model_path):
        print(f"Please download the model and place it in '{model_path}' directory.")
        return
    model = Model(model_path)

    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8000)
    stream.start_stream()

    # Create a recognizer object
    recognizer = KaldiRecognizer(model, 16000)

    print("Speech recognition started. Speak into the microphone...")
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print(result)
        else:
            partial = recognizer.PartialResult()
            print(partial)

if __name__ == "__main__":
    continuous_speech_to_text()
