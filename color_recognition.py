def color_recognition():
    import cv2
    import mediapipe as mp
    import sys
    import pyfirmata
    import time 
    import pyttsx3
    friend = pyttsx3.init()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    board = pyfirmata.ArduinoMega('COM7')

    p = [0 for i in range(21)]  
    finger = [0 for i in range(4)]  

    i1, i2, i3 = 0, 0, 0


    def distance(point1, point2):
        return abs(point1 - point2)


    while True:
        good, img = cap.read()
        
        if not good:
            print("...")
            break

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                for id, point in enumerate(handLms.landmark):
                    width, height, color = img.shape
                    width, height = int(point.x * height), int(point.y * width)
                    p[id] = height
                    
                dist8 = distance(p[4], p[8])
                dist12 = distance(p[4], p[12])
                dist16 = distance(p[4], p[16])
                
        _, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape

        cx = int(width / 2)
        cy = int(height / 2)

        # Pick pixel value
        pixel_center = hsv_frame[cy, cx]
        hue_value = pixel_center[0]

        color = "Undefined"
        if hue_value < 5:
            color = "RED"
            board.digital[5].write(0)
            board.digital[6].write(0)
            #friend.say("RED")
            #friend.runAndWait()

        elif hue_value < 22:
            color = "ORANGE"
            board.digital[5].write(0)
            board.digital[6].write(0)
            #friend.say("ORANGE")
            #friend.runAndWait()

        elif hue_value < 33:
            color = "YELLOW"
            board.digital[5].write(0)
            board.digital[6].write(0)
            #friend.say("YELLOW")
            #friend.runAndWait()
        elif hue_value < 78:
            color = "GREEN"
            board.digital[6].write(1)
            board.digital[5].write(0)
            #friend.say("GREEN")
            #friend.runAndWait()
        elif hue_value < 131:
            color = "BLUE"
            board.digital[6].write(0)
            board.digital[5].write(1)
            #friend.say("BLUE")
            #friend.runAndWait()
        elif hue_value < 170:
            board.digital[5].write(0)
            board.digital[6].write(0)
            color = "VIOLET"
            #friend.say("VIOLET")
            #friend.runAndWait()
        else:
            color = "RED"
            board.digital[5].write(0)
            board.digital[6].write(0)
            #friend.say("VIOLET")
            #friend.runAndWait()



        pixel_center_bgr = frame[cy, cx]
        b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

        cv2.rectangle(frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1)
        cv2.putText(frame, color, (cx - 200, 100), 0, 3, (b, g, r), 5)
        cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)



        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break



    cap.release()
    cv2.destroyAllWindows()