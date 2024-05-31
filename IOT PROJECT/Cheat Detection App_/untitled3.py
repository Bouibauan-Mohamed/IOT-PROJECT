from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import os
import subprocess
from PyQt5.uic import loadUiType

import threading
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QTextBrowser
import sys
import os
import subprocess
from model_sign_to_text import model_sign_to_text
from model_sign_to_text2 import model_sign_to_text2
from PyQt5.uic import loadUiType
from voiceRecognition import VoiceRecognition

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import os
import subprocess
from PyQt5.uic import loadUiType
from voiceRecognition import VoiceRecognition

MainUI, _ = loadUiType('main_pfa.ui')

class Main(QMainWindow, MainUI):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.handle_buttons()
        self.voice_recognition = None  # Initialiser comme None
        QMessageBox.information(self, "Bienvenue", "Bienvenue dans la plateforme d'examen")
        QTimer.singleShot(1000, self.show_identification_message)

    def handle_buttons(self):
        self.pushButton_5.clicked.connect(self.start_face_recognition)
        self.pushButton_4.clicked.connect(self.start_object_detection)
        self.pushButton_6.clicked.connect(self.finish_exam)  # Bouton pour terminer l'examen

    def show_identification_message(self):
        QMessageBox.information(self, "Identification", "L'identification va commencer.")
        self.start_face_recognition()

    def start_face_recognition(self):
        self.recognizer = model_sign_to_text2()
        success = self.recognizer.run_recognition()
        if success:
            self.show_exam_session_message()
        else:
            QMessageBox.critical(self, "Échec", "Vous n'avez pas la permission de passer l'examen, triche !!!")

    def show_exam_session_message(self):
        reply = QMessageBox.information(self, "Succès", "Identification avec succès. Cliquez sur OK pour entrer dans la session d'examen.", QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            self.open_pdf_file("exame.pdf")
            self.start_exam_monitoring()

    def open_pdf_file(self, file_path):
        if sys.platform == "win32":
            os.startfile(file_path)
        elif sys.platform == "darwin":  # macOS
            subprocess.call(["open", file_path])
        else:  # Linux variants
            subprocess.call(["xdg-open", file_path])

    def start_exam_monitoring(self):
        # Lancer la détection d'objets et la reconnaissance vocale en parallèle
        threading.Thread(target=self.start_object_detection).start()
        threading.Thread(target=self.start_voice_recognition).start()

    def start_object_detection(self):
        self.detector = model_sign_to_text()
        self.detector.run_detection()

    def start_voice_recognition(self):
        doc_path = "./Questions_QCM.docx"  # Chemin du document contenant les mots-clés
        
        # Vérifier si le fichier existe
        if not os.path.isfile(doc_path):
            print(f"Erreur : Le fichier {doc_path} n'a pas été trouvé.")
            return  # Sortir si le fichier n'est pas trouvé

        # Créer une instance de la classe VoiceRecognition
        self.voice_recognition = VoiceRecognition(doc_path)

        # Durée pendant laquelle vous voulez écouter (en secondes)
        duration = 3600  # ou la durée que vous souhaitez

        # Démarrer l'écoute
        self.voice_recognition.listen(duration)

    def finish_exam(self):
        # Arrêter la reconnaissance vocale et la détection d'objets
        if self.voice_recognition:
            self.voice_recognition.stop()

        # Afficher la liste des mots-clés détectés à la fin de l'examen
        if self.voice_recognition and self.voice_recognition.detected_keywords:
            QMessageBox.information(self, "Mots-clés détectés", "Liste des mots-clés détectés :\n" + "\n".join(self.voice_recognition.detected_keywords))
        else:
            QMessageBox.information(self, "Mots-clés détectés", "Aucun mot-clé détecté.")

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
