import numpy as np
import cv2

class model_sign_to_text:
    def __init__(self):
        self.thres = 0.5  # Seuil pour détecter l'objet
        self.nms_threshold = 0.2
        self.classNames = []
        self.detected_objects = []  # Liste pour stocker les objets détectés

        with open('objects.txt', 'r') as f:
            self.classNames = f.read().splitlines()

        # Initialiser les couleurs pour chaque classe détectée
        self.Colors = np.random.uniform(0, 255, size=(len(self.classNames), 3))

        # Charger le modèle de détection d'objets
        weightsPath = "frozen_inference_graph.pb"
        configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        self.net = cv2.dnn_DetectionModel(weightsPath, configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

    def detect_objects(self, img):
        classIds, confs, bbox = self.net.detect(img, confThreshold=self.thres)
        bbox = list(bbox)
        confs = list(np.array(confs).reshape(1, -1)[0])
        confs = list(map(float, confs))
        
        indices = cv2.dnn.NMSBoxes(bbox, confs, self.thres, self.nms_threshold)
        
        self.detected_objects = []  # Réinitialiser la liste des objets détectés

        if indices is not None and len(indices) > 0:
            indices = np.array(indices).flatten()
            for i in indices:
                if i < len(bbox) and i < len(classIds):
                    box = bbox[i]
                    classId = classIds[i] - 1
                    if classId >= 0 and classId < len(self.classNames):
                        self.detected_objects.append(self.classNames[classId])  # Ajouter l'objet détecté
                        color = [int(c) for c in self.Colors[classId]]
                        confidence = str(round(confs[i], 2))
                        x, y, w, h = box
                        cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness=2)
                        cv2.putText(img, f"{self.classNames[classId]} {confidence}", (x + 10, y + 20), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)
        
        return img



    def run_detection(self):
        # Modifier ici pour utiliser l'URL de DroidCam
        cap = cv2.VideoCapture('http://192.168.18.11:4747/video')
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 100)

        while True:
            success, img = cap.read()
            if not success:
                break

            img = self.detect_objects(img)
            cv2.imshow("Output", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    detector = model_sign_to_text()
    detector.run_detection()
