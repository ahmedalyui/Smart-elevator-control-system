import cv2
import numpy as np
import face_recognition
import os

path = "/home/mahana/code/ras pi/Face-recognition-python-project-main/persons"

images = []
classNames = []

personsList = os.listdir(path)

for cl in personsList:
    curPerson = cv2.imread(f'{path}/{cl}')
    images.append(curPerson)
    classNames.append(os.path.splitext(cl)[0])

print("classNames:", classNames)


def findEncodings(images):
    encodeList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


encodeListKnown = findEncodings(images)
print("Encoding Complete")

cap = cv2.VideoCapture(0)

name = "unknown"

while True:
    success, img = cap.read()
    if not success:
        continue

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurentFrame = face_recognition.face_locations(imgS)
    encodeCurentFrame = face_recognition.face_encodings(imgS, faceCurentFrame)

    for encodeFace, faceLoc in zip(encodeCurentFrame, faceCurentFrame):

        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:

            name = classNames[matchIndex].upper()
            name = "".join([c for c in name if not c.isdigit()])

        else:
            name = "unknown"

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)

        cv2.putText(img, name, (x1 + 6, y2 - 6),
                    cv2.FONT_HERSHEY_COMPLEX, 1,
                    (255, 255, 255), 2)

    print(name)

    cv2.imshow('Face Recognition', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()