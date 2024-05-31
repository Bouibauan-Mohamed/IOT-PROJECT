import face_recognition
import cv2
import numpy as np
import time

class model_sign_to_text2:
    def __init__(self):
        # Initialisation de la webcam
        self.video_capture = cv2.VideoCapture(0)

        # Initialisation des noms et des encodages de visages connus
        self.known_face_encodings = []
        self.known_face_names = ["Mohamed", "Hassan", "Doha", "Kawtar"]
        image_files = ["images/bouibauan.png", "images/hassan.jpeg", "images/Doha.jpeg", "images/Kawtar.jpeg"]

        for image_file, name in zip(image_files, self.known_face_names):
            image = face_recognition.load_image_file(image_file)
            face_encoding = face_recognition.face_encodings(image)[0]
            self.known_face_encodings.append(face_encoding)

        # Initialisation de variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def run_recognition(self):
        start_time = time.time()  # Début du comptage du temps
        permission_granted = False

        while True:
            # Capture d'une seule frame de la vidéo
            ret, frame = self.video_capture.read()

            # Redimensionnement de la frame de vidéo pour un traitement plus rapide
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Conversion de l'image de couleur BGR (utilisée par OpenCV) en couleur RGB (utilisée par face_recognition)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Traitement d'une frame sur deux pour gagner du temps
            if self.process_this_frame:
                # Trouver tous les visages et encodages de visages dans la frame actuelle de la vidéo
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        permission_granted = True

                    self.face_names.append(name)

            self.process_this_frame = not self.process_this_frame

            # Affichage des résultats
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('Video', frame)

            # Contrôle du temps écoulé et décision sur la permission
            if (time.time() - start_time) > 5:  # 5 secondes sont passées
                self.video_capture.release()
                cv2.destroyAllWindows()
                return permission_granted

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.video_capture.release()
        cv2.destroyAllWindows()
        return permission_granted

if __name__ == '__main__':
    recognizer = model_sign_to_text2()
    result = recognizer.run_recognition()
    if result:
        print("Accès autorisé.")
    else:
        print("Accès refusé.")
