import face_recognition

#Carrega as imagens para comparação
image1 = face_recognition.load_image_file("Facial_Recognition/trainingImages/imagem3.jpg")
image2 = face_recognition.load_image_file("Facial_Recognition/trainingImages/imagem4.jpg")

#extrai os dados faciais da imagem
dados_image1 = face_recognition.face_encodings(image1)[0]
dados_image2 = face_recognition.face_encodings(image2)[0]

#calcula a distância entre as duas imagens
distance = face_recognition.face_distance([dados_image1], dados_image2)[0]

#define limite para a distância
limit = 0.6

#realiza comparação
if distance < limit:
    print("As faces correspondem")
else:
    print("As faces NÃO correspondem")