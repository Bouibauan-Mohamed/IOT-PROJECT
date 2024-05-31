import time
from voiceRecognition import VoiceRecognition

if __name__ == "__main__":
    # Chemin du document contenant les questions
    doc_path = "./Questions_QCM.docx"
    

    # Créer une instance de la classe VoiceRecognition
    voice_recognition = VoiceRecognition(doc_path)

    
    # Durée pendant laquelle vous voulez écouter (en secondes)
    duration = 60

    # Démarrer l'écoute
    voice_recognition.listen(duration)

    # Attendez que l'écoute se termine
    time.sleep(duration)

    # Afficher le nombre de mots-clés détectés
    print("Nombre de mots-clés détectés:", voice_recognition.keyword_count)

