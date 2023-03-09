import cv2
import time
import HandTrackingModule

wCam,hCam = 840,1040
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

imgRead = cv2.imread('Fingers/images.jfif')
img1 = imgRead[0:142,0:69]
img2 = imgRead[0:142,69:138]
img3 = imgRead[0:142,138:207]
img4 = imgRead[0:142,207:276]
img5 = imgRead[0:142,276:345]
overLayList = [img1 , img2 , img3 ,img4 , img5]


pTime = 0

detector = HandTrackingModule.handDetector(detectionCon=1)
tipIds = [4,8,12,16,20]
while True:
    succces, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    lmList = lmList[0]
    totalFingers = 0
    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)
    if (totalFingers - 1) >= 0:
        h,w,c = overLayList[totalFingers - 1].shape
        img[0:h,0:w] = overLayList[totalFingers - 1]

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN , 3 , (255,0,0) , 3)

    cv2.imshow("Image",img)
    cv2.waitKey(1)

