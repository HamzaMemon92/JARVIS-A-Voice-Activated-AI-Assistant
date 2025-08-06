import speech_recognition as sr
import webbrowser
import pyttsx3
import mymusic
import time
import requests
from client import gemini_process_command  

engine = pyttsx3.init()

newsapi = "your_api_key"  

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    print("command received:", c)

    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")

    elif "open indian ai" in c.lower():
        webbrowser.open("https://www.perplexity.ai")

    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")

    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com")

    elif "open ai" in c.lower():
        webbrowser.open("https://openai.com/index/chatgpt/")

    elif "linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = mymusic.mymusic.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in your music list.")

    elif "news" in c.lower():
        print("Fetching news...")
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            if r.status_code == 200:
                articles = r.json().get("articles", [])
                for article in articles[:5]:
                    speak(article['title'])
            else:
                speak("Unable to fetch news.")
        except Exception as e:
            print("News API Error:", e)
            speak("Sorry, I couldn't fetch the news.")

    else:
        print("Command not recognized, forwarding to Gemini AI...")
        try:
            response = gemini_process_command(c)
            print("Gemini says:", response)
            speak(response)
        except Exception as e:
            print("Gemini Error:", e)
            speak("Sorry, Gemini couldn't understand.")

if __name__ == "__main__":
    speak("INITIALIZING JARVIS ....")

    while True:
        r = sr.Recognizer()
        print("Recognizing...")

        try:
            with sr.Microphone() as source:
                print("Hearing")
                audio = r.listen(source, timeout=60, phrase_time_limit=50)

            word = r.recognize_google(audio)

            if "jarvis" in word.lower():
                time.sleep(0.5)
                speak("Yes master")
                time.sleep(1.2)
                speak("Listening...")

                with sr.Microphone() as source:
                    print("Agent active")
                    r.adjust_for_ambient_noise(source, duration=0.5)  # auto-calibrate mic
                    audio = r.listen(source, timeout=60, phrase_time_limit=50)  # longer capture

                command = r.recognize_google(audio)
                processCommand(command)

        except Exception as e:
            print("Error:", e)

