import pyfirmata
import time
import cv2
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.HandTrackingModule import HandDetector
import time
import numpy as np

# SET UP ARDUINO
arduino = pyfirmata.ArduinoMega("COM7")
cap = cv2.VideoCapture(1)
lenPin = arduino.get_pin('d:7:p') # PWM Pin
print("Starting to output PWM signal")

# SET UP DETECTOR
cap = cv2.VideoCapture(1)
handDetector = HandDetector(detectionCon=0.7, maxHands=2)
faceDetector = FaceDetector()
# ubah ukuran video 
print("Starting Camera")
cap.set(3, 720)
cap.set(4, 480)

# Range distance fingger detection
maxDistance = 200
minDistace  = 50
# range Rectangle
minRect = 150
maxRect = 400

while True:
 # Detect wajah dan tangan
    succes, img = cap.read()
    img, bboxs = faceDetector.findFaces(img)
    hands, img = handDetector.findHands(img) 
    # tampilkan kotak dan text ketika pertama kali dijalankan
    cv2.rectangle(img, (50,150), (100, 400), (0,255,0), 3)

# jika terdeteksi wajah
    if bboxs:
        lenPin.write(256/256)
        cv2.putText(img, f"Lamp ON", (300, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,255))


        if hands:
            hand1 = hands[0]
            imList = hand1["lmList"]  # List of 21 Landmark points

            #find Distance
            length, info, img = handDetector.findDistance(imList[8], imList[4], img)
            
            #Convert nilai antara distance dan rectangle / rectangle dan persentase
            valueRect = np.interp(length, [minDistace, maxDistance], [maxRect, minRect])
            valPersen = np.interp(valueRect, [minRect, maxRect], [100, 0])
            # Covert nilai Persentase dan nilai value brightness 
            valBrigt = np.interp(valPersen, [0, 100], [0, 255])
            
            print(valBrigt)
            lenPin.write(valBrigt/256)

            cv2.rectangle(img, (50,round(valueRect)), (100, 400), (0,255,0), cv2.FILLED)
            cv2.putText(img, f"{round(valPersen)} %", (45, 130), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0,255,0))
        

    else:
        lenPin.write(0/256)
        cv2.putText(img, f"Lamp OFF", (300, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,255))
# ----------------------- 

    cv2.imshow('image', img)
    cv2.waitKey(1)
