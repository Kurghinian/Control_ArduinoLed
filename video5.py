def video(): #Ստեղծում ենք Video անունով ֆունկցիա 
    import mediapipe as mp #Կանչում ենք Գրադարանները
    import cv2 as cv
    import sys
    import pyfirmata
    import time 


    cap = cv.VideoCapture(0) #Միացնում ենք տեսախցիկը
    if not cap.isOpened():
        print("Cannot open camera")
        sys.exit()

    mpHands = mp.solutions.hands 
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    board = pyfirmata.ArduinoMega('COM7') #Միանում ենք Arduino-ին


    p = [0 for i in range(21)]  
    finger = [0 for i in range(4)]  

    i1 = 0
    i2 = 0
    i3 = 0


    def distance(point1, point2):
        return abs(point1 - point2)

    board.digital[9].write(1)

    while True:
        good, img = cap.read()
        
        if not good:
            print("...")
            break
        
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                for id, point in enumerate(handLms.landmark):
                    width, height, color = img.shape
                    width, height = int(point.x * height), int(point.y * width)
                    p[id] = height

            #################################
                dist8 = distance(p[4], p[8])#### Ստացնում ենք մատների հեռավորությունը
                dist12 = distance(p[4], p[12])##
                dist16 = distance(p[4], p[16])##
                ################################
                
                if 20 > dist8 < min(dist12, dist16):
                    if i1 == 0: # Այս պայմանը կատարվում է որպեսզի լույսը միացրած մնա այնքան ժամանակ մինչև մատները նորից չհպվեն իրար
                        i1 = 1
                    else:
                        i1 =0
                    board.digital[5].write(i1)
                    time.sleep(1)
                if dist12 < min(dist8, dist16):
                    if i2 == 0:
                        i2 = 1
                    else:
                        i2 = 0            
                    board.digital[6].write(i2)
                    time.sleep(1)
                if dist16 < min(dist12, dist8):
                    if i3 ==0:
                        i3 = 1
                    else:
                        i3= 0
                    board.digital[8].write(i2)
                    time.sleep(1)
        cv.imshow('frame', img)
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()