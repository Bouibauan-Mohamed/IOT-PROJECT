import cv2

def access_droidcam():
    # Le port utilisé par DroidCam (le port par défaut est généralement 4747 pour le flux vidéo)
    droidcam_url = 'http://192.168.46.153:4747/video'  # Si vous utilisez Wi-Fi
    # droidcam_url = 'http://IP_OF_YOUR_PHONE:4747/video'  # Remplacez IP_OF_YOUR_PHONE par l'IP affichée sur DroidCam sur votre téléphone.

    # Capturer le flux vidéo
    cap = cv2.VideoCapture(droidcam_url)
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            # Affichage de la frame
            cv2.imshow('DroidCam Stream', frame)

            # Arrêter le flux en appuyant sur 'q'
            if cv2.waitKey(1) == ord('q'):
                break
    finally:
        # Quand tout est fini, relâcher la capture
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    access_droidcam()
