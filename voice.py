import pyttsx3
import speech_recognition as sr
import wikipedia
import wolframalpha

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def search(query):
    print(f"🔎 Searching for: {query}")  # Debugging

    try:
        app_id = "Your WolframAlpha App ID here"  # Replace with actual App ID
        client = wolframalpha.Client(app_id)
        res = client.query(query)
        answer = next(res.results).text
        print(f"✅ Answer: {answer}")
        SpeakText("Your answer is " + answer)
    except Exception as e:
        print(f"❌ WolframAlpha failed: {e}")
        SpeakText("I am searching for " + query)
        try:
            wiki_summary = wikipedia.summary(query, sentences=3)
            print(f"🌐 Wikipedia: {wiki_summary}")
            SpeakText(wiki_summary)
        except Exception as e:
            print(f"❌ Wikipedia search failed: {e}")
            SpeakText("I couldn't find anything.")

# 🎤 Voice Input
print("🎤 Say something or type your query:")
query = input().strip().lower()

if not query:
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🛠 Adjusting for noise... Speak now!")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        try:
            print("🎤 Listening (Timeout: 5s)...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Added timeouts
            print("🎧 Processing...")

            query = recognizer.recognize_google(audio)
            print(f"🎙 You said: {query}")

        except sr.WaitTimeoutError:
            print("⏳ Timeout: No speech detected.")
        except sr.UnknownValueError:
            print("❌ Could not understand the audio.")
        except sr.RequestError as e:
            print(f"❌ Google API error: {e}")



# If we have a query, search it
if query:
    search(query)
else:
    print("⚠️ No query provided. Exiting.")
