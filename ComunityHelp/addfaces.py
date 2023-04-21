import cv2, dlib, face_recognition, json, asyncio
import numpy as np

# Carrega as imagens e os nomes das pessoas conhecidas
try:
    jsonNames = open('./reconhecimentoTempoReal/nomes.json', 'r')
    known_names = json.load(jsonNames)
    jsonNames.close()

    known_faces = np.loadtxt('./reconhecimentoTempoReal/faces.txt')
    print(f'\tnomes = {known_names}\n\tfaces = {known_faces}')
except:    
    known_faces = []
    known_names = []
    print('skip')

def addFace(name, pathImage):
    global known_faces

    image = face_recognition.load_image_file(pathImage)
    face_encoding = face_recognition.face_encodings(image)[0]
    print(type(face_encoding))
    #known_faces = np.append(known_faces, face_encoding)
    _known_faces = np.concatenate((known_faces, np.expand_dims(face_encoding, axis = 0)), axis = 0)
    known_names.append(name)
    print(_known_faces)
    
    np.savetxt('./reconhecimentoTempoReal/faces.txt', _known_faces)

    jsonNames = open('./reconhecimentoTempoReal/nomes.json', 'w')
    json.dump(known_names, jsonNames)
    jsonNames.close()