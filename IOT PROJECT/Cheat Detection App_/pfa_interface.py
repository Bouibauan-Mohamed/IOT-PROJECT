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
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

MainUI, _ = loadUiType('main_pfa.ui')
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
            self.open_pdf_file("b.html")
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

    def create_pdf_report(self, message, is_cheating):
        pdf_path = "examen_analysis.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        normal_style = styles["BodyText"]

        # Ajouter le titre du document
        title = Paragraph("Analyse et rapport de l'Examen", title_style)
        elements.append(title)

        # Créer les données du tableau
        data = [
            ["Résultats", "Détails"],
            ["Message", message],
            ["Triche détectée", "Oui" if is_cheating else "Non"]
        ]

        # Style pour le tableau
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        # Créer le tableau
        table = Table(data)
        table.setStyle(table_style)

        # Ajouter le tableau aux éléments du PDF
        elements.append(table)

        # Construire le document PDF
        doc.build(elements)
        print(f"PDF report created: {pdf_path}")

    def finish_exam(self):
        if self.voice_recognition:
            self.voice_recognition.stop()

        if self.voice_recognition and self.voice_recognition.detected_keywords:
            detected_keywords = "\n".join(self.voice_recognition.detected_keywords)
        else:
            detected_keywords = "Aucun mot-clé détecté."

        if self.detector and self.detector.detected_objects:
            detected_objects = "\n".join(self.detector.detected_objects)
        else:
            detected_objects = "Aucun objet détecté."

        # Définir un seuil pour la détection de triche
        keyword_threshold = 2
        object_threshold = 2

        is_cheating = (len(self.voice_recognition.detected_keywords) > keyword_threshold or 
                       len(self.detector.detected_objects) > object_threshold)

        if is_cheating:
            cheating_message = "Triche détectée !"
        else:
            cheating_message = "Pas de triche détectée."

        message = (f"Mots-clés détectés :\n{detected_keywords}\n\n"
                   f"Objets détectés :\n{detected_objects}\n\n"
                   f"{cheating_message}")

        # Créer le rapport PDF
        self.create_pdf_report(message, is_cheating)

        # Afficher le message dans une boîte de dialogue
        QMessageBox.information(self, "Résultats de l'examen", message)


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
