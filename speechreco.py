from google.cloud import speech
import pyaudio
import queue

# Initialize Google Cloud Speech client and audio stream configurations
client = speech.SpeechClient()
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
)
streaming_config = speech.StreamingRecognitionConfig(config=config)

# Audio stream generator for microphone input
def get_audio_stream():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    while True:
        yield stream.read(1024)

# Stream transcription
def transcribe_audio():
    audio_stream = get_audio_stream()
    requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_stream)
    responses = client.streaming_recognize(config=streaming_config, requests=requests)

    print("Listening... (speak into the microphone)")
    with open("output.txt", "w") as output_file:  # Save transcriptions to a file
        for response in responses:
            for result in response.results:
                transcript = result.alternatives[0].transcript
                print("Transcript:", transcript)
                output_file.write(transcript + "\n")  # Save each transcription line
                output_file.flush()

transcribe_audio()
