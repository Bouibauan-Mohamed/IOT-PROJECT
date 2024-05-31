import threading
from docx import Document
import speech_recognition as sr
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Télécharger les stopwords et le modèle WordNet pour la première fois
nltk.download('stopwords')
nltk.download('wordnet')

class VoiceRecognition:
    def __init__(self, doc_path):
        self.recognizer = sr.Recognizer()
        self.keywords = self.load_keywords(doc_path)
        self.keyword_count = 0
        self.detected_keywords = []
        self.stop_listening = False

    def load_keywords(self, path):
        doc = Document(path)
        keywords = []
        stop_words = set(stopwords.words('french'))  # Assurez-vous d'avoir installé 'stopwords' pour le français
        lemmatizer = WordNetLemmatizer()
        
        for para in doc.paragraphs:
            words = para.text.split()
            for word in words:
                word = word.translate(str.maketrans('', '', string.punctuation))
                word = lemmatizer.lemmatize(word.lower())
                if word and word not in stop_words:
                    keywords.append(word)
        
        return set(keywords)

    def listen(self, duration):
        self.stop_listening = False  # Réinitialiser l'attribut pour arrêter l'écoute
        thread = threading.Thread(target=self.threaded_listen, args=(duration,))
        thread.start()

    def threaded_listen(self, duration):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Start listening...")
            start_time = threading.Event()
            start_time.set()  # Utiliser un événement pour contrôler le timing
            while not self.stop_listening and start_time.is_set():
                try:
                    audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=10)  # Réécouter toutes les 10 secondes
                    self.handle_audio(audio)
                except sr.WaitTimeoutError:
                    print("Listening timed out, continuing...")  # Continue d'écouter
            print("Stopped listening.")

    def handle_audio(self, audio):
        try:
            text = self.recognizer.recognize_google(audio, language='fr-FR')
            print("Heard:", text)
            self.process_keywords(text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Service error; {e}")

    def process_keywords(self, text):
        words = text.lower().split()
        for word in words:
            if word in self.keywords:
                self.keyword_count += 1
                self.detected_keywords.append(word)
                print(f"Keyword detected: {word}")

    def stop(self):
        self.stop_listening = True  # Méthode pour arrêter l'écoute
