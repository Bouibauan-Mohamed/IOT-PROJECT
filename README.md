# IOT-PROJECT
Une application polyvalente combinant reconnaissance faciale, détection vocale, détection d'objets en temps réel et surveillance de la triche. Elle utilise des bibliothèques spécialisées comme face_recognition et speech_recognition, avec une interface intuitive construite en PyQt5.

Voici une description succincte de l'application :

# Identification faciale :

Utilisation de la bibliothèque face_recognition pour la reconnaissance faciale.
La bibliothèque utilise le modèle de reconnaissance faciale de dlib basé sur un réseau neuronal convolutif (CNN) pour l'encodage des visages.
Deux modèles disponibles : HOG (rapide et précis dans des conditions contrôlées) et CNN (plus précis mais plus lent, recommandé pour les environnements avec des variations d'éclairage et des angles de vue variés).
Détection et transcription vocale :

Utilisation de la bibliothèque speech_recognition pour la reconnaissance vocale.
Utilisation de NLTK pour le traitement du langage naturel afin d'extraire intelligemment des mots-clés en lemmatisant les mots-clés extraits et en supprimant les mots vides.
# Détection d'objets :

Choix du modèle SSD MobileNet V3 pour sa légèreté, adaptée aux projets avec des ressources limitées.
Utilisation de l'application DroidCam pour la détection d'objets en streaming, nécessitant une demande d'adresse IP pour connecter l'appareil mobile à l'ordinateur via le même réseau local.
Application de bureau en Python utilisant la bibliothèque PyQt5 :

# L'application détecte la triche.
Cette application combine plusieurs fonctionnalités telles que la reconnaissance faciale, la détection et la transcription vocale, la détection d'objets, ainsi qu'une application de bureau pour détecter la triche.

!!!!!!!!!!!!!!!!!!!  RUN Application !!!!!!!!!!!!!!!!!!!!!!!
===>Dirigez-vous vers le répertoire "PROJECT\Cheat Detection App\pfa_interface.py


![interface](https://github.com/Bouibauan-Mohamed/IOT-PROJECT/assets/102635115/cc9898a8-3ecf-4071-b88d-cefad5438291)
