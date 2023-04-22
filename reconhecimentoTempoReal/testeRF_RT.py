import cv2, dlib, face_recognition, json, asyncio
import numpy as np

# Carrega o modelo de detector de faces do dlib
detector = dlib.get_frontal_face_detector()

# Carrega a imagem e converte para RGB
imagem = cv2.imread('./trainingImages/pessoa1.jpg')
imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

# Carrega o modelo de codificação de faces
modelo_codificacao = 'modelo_de_reconhecimento_de_faces.dat'
codificacoes_conhecidas = face_recognition.face_encodings(imagem_rgb, model=modelo_codificacao)

# Carrega as imagens e os nomes das pessoas conhecidas
try:
    jsonNames = open('./reconhecimentoTempoReal/nomes.json', 'r')
    known_names = json.load(jsonNames)
    jsonNames.close()

    known_faces = np.loadtxt('./reconhecimentoTempoReal/faces.txt')
    print(f'\tnomes = {known_names}\n\tfaces = {known_faces}')
    print(type(known_faces))
except:
    known_faces = []
    known_names = []
    print('skip')

##ADICIONA AS PESSOAS A SEREM RECONHECIDAS NO SISTEMA

# image1 = face_recognition.load_image_file("Facial_Recognition/reconhecimentoTempoReal/pessoa1.jpg")
# face_encoding1 = face_recognition.face_encodings(image1)[0]
# known_faces.append(face_encoding1)
# known_names.append("Allan")

# image2 = face_recognition.load_image_file("Facial_Recognition/reconhecimentoTempoReal/imagemedu.jpg")
# face_encoding2 = face_recognition.face_encodings(image2)[0]
# known_faces.append(face_encoding2)
# known_names.append("esquilo")

# image3 = face_recognition.load_image_file("Facial_Recognition/reconhecimentoTempoReal/imagem2.jpg")
# face_encoding3 = face_recognition.face_encodings(image3)[0]
# known_faces.append(face_encoding3)
# known_names.append("pessoa 3")

def addFace(name, pathImage):
    global known_faces

    if name in known_names:
        print("já foi registrado")
        
    else:
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


#addFace("FellipeTESTE", "./trainingImages/imagem2.jpg")
#addFace("esquilo", "./trainingImages/imagemedu.jpg")
#addFace("AllanTESTE", "./trainingImages/pessoa1.jpg")

# Inicializa a captura de vídeo da câmera
cap = cv2.VideoCapture(0)

while True:
    # Captura uma imagem da câmera
    ret, frame = cap.read()

    #redimensiona a imagem pra otimizar a captura
    #small_frame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)
    small_frame = frame

    # Converte a imagem para escala de cinza
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

    # Detecta as faces na imagem
    faces = detector(gray)

    if len(faces) == 0:
        pass
    else:

        # Itera sobre as faces detectadas
        for face in faces:
            name = "Desconhecido"

            # Extrai as características da face
            face_locations = face_recognition.face_locations(small_frame)
            if face_locations:
                face_encoding = face_recognition.face_encodings(small_frame, [face_locations[0]])[0]

                # Compara as características da face com as faces conhecidas
                matches = face_recognition.compare_faces(known_faces, face_encoding)

                # Identifica o nome da pessoa reconhecida
                if True in matches:
                    index = matches.index(True)
                    name = known_names[index]
                    print(f'{name} entrou!')

            # Desenha um retângulo em volta da face e o nome da pessoa reconhecida
            top, right, bottom, left = face.top(), face.right(), face.bottom(), face.left()
            cv2.rectangle(small_frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(small_frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Mostra a imagem com as faces detectadas e reconhecidas
    cv2.imshow("Video", small_frame)

    # Sai do loop se a tecla "q" for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha a janela de exibição
cap.release()
cv2.destroyAllWindows()
