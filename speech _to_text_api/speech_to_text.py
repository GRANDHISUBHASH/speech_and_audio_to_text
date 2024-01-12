from dotenv import load_dotenv
from openai import OpenAI
import os
import speech_recognition as sr

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(r, file_path):
    try:
        with sr.AudioFile(file_path) as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)
            transcript = r.recognize_google(audio)
            return transcript
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    except sr.UnknownValueError:
        print("Unknown error occurred")
        return None

def main():
    print("Welcome to the Speech-to-Text Game!")
    
    while True:
        print("\nChoose an option:")
        print("0: Speech-to-Text")
        print("1: Audio File to Text")
        print("2: Exit")

        choice = input("Enter your choice (0, 1, or 2): ")

        if choice == "0":
            try:
                print("\nSpeak something...")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.2)
                    audio = r.listen(source)
                    speech_text = r.recognize_google(audio)
                    print("You said:", speech_text)
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
            except sr.UnknownValueError:
                print("Unknown error occurred")

        elif choice == "1":
            audio_file_path = input("Enter the path to the audio file: ")
            if os.path.exists(audio_file_path):
                openai_transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=open(audio_file_path, "rb"),
                    response_format="text"
                )
                print("\nOpenAI Transcript:", openai_transcript)

                speech_recognition_transcript = transcribe_audio(r, audio_file_path)
                print("SpeechRecognition Transcript:", speech_recognition_transcript)
                
            else:
                print("Error: File not found. Please provide a valid file path.")

        elif choice == "2":
            print("Exiting the Speech-to-Text Game. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 0, 1, or 2.")

if __name__ == "__main__":
    r = sr.Recognizer()
    main()
