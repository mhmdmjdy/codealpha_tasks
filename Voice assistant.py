import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.weather_api_key = "YOUR_OPENWEATHERMAP_API_KEY"

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            command = self.recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

    def understand(self, command):
        if not command:
            return "retry"
        if "time" in command:
            return "get_time"
        elif "weather" in command:
            return "get_weather"
        elif "play music" in command or "play song" in command:
            return "play_music"
        elif "search for" in command:
            return "google_search"
        elif "exit" in command:
            return "exit"
        else:
            return "unknown"

    def execute_task(self, task):
        if task == "get_time":
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}.")
        elif task == "get_weather":
            self.get_weather()
        elif task == "play_music":
            self.play_youtube_song()
        elif task == "google_search":
            self.google_search()
        elif task == "exit":
            self.speak("Goodbye!")
            exit()
        elif task == "retry":
            pass  
        else:
            self.speak("Sorry, I didn't understand that.")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def play_youtube_song(self):
        self.speak("Sure! What song would you like to listen to?")
        song_name = self.listen()
        self.speak(f"Searching for {song_name} on YouTube...")
        query = song_name.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)

    def get_weather(self):
        self.speak("Sure! Please provide the city name.")
        city = self.listen()
        if city:
            weather_data = self.fetch_weather_data(city)
            if weather_data:
                weather_description = weather_data["weather"][0]["description"]
                temperature = weather_data["main"]["temp"]
                self.speak(f"The weather in {city} is currently {weather_description} with a temperature of {temperature} degrees Celsius.")
            else:
                self.speak("Sorry, I couldn't fetch the weather data. Please try again later.")

    def fetch_weather_data(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def google_search(self):
        self.speak("What would you like to search for?")
        search_query = self.listen()
        if search_query:
            self.speak(f"Searching Google for {search_query}")
            url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
            webbrowser.open(url)

def main():
    assistant = VoiceAssistant()
    assistant.speak("Hello! I'm your Python voice assistant. How can I assist you today?")

    while True:
        command = assistant.listen()
        task = assistant.understand(command)
        assistant.execute_task(task)

if __name__ == "__main__":
    main()
