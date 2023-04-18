import cv2 as cv
import mediapipe as mp
import time
import math


class HandLandmarks:
    def __init__(self, static_img=False, maxhands=1, mincon=0.5, mintrack=0.5):
        self.capture = cv.VideoCapture(0)
        self.capture.set(3, 640)
        self.capture.set(4, 480)

        self.frame_width, self.frame_height = 640, 480
        self.frameR = 100
        self.Ptime = 0
        self.face_d = False
        self.draw = True
        # mp_drawing_styles = mp.solutions.drawing_styles                 ---for styles
        self.mp_drawing_utils = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.mp_face_detection = mp.solutions.face_detection
        self.hand_detector = self.mp_hands.Hands(static_image_mode=static_img, max_num_hands=maxhands,  # for no.of hands change here
                                                 min_detection_confidence=mincon, min_tracking_confidence=mintrack)

        #self.screen_width, self.screen_height = pag.size()
        self.finger_tips = [4, 8, 12, 16, 20]
        self.i = 0

    def handDetector(self, click_i=False, click_r=False):
        hand_list, xList, yList = [], [], []

        _, frame = self.capture.read()
        frame = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        result = self.hand_detector.process(rgb_frame)
        hands = result.multi_hand_landmarks
        handed = result.multi_handedness

        with self.mp_face_detection.FaceDetection(
                model_selection=0, min_detection_confidence=0.5) as face_detection:
            results = face_detection.process(frame)
            if results.detections:
                if self.draw == True:
                    for detection in results.detections:
                        self.mp_drawing_utils.draw_detection(frame, detection)
                self.face_d = True

        Ctime = time.time()
        fps = 1/(Ctime-self.Ptime)
        self.Ptime = Ctime
        if self.draw == True:
            cv.putText(frame, str(int(fps)), (10, 40),
                       cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            cv.rectangle(frame, (self.frameR, self.frameR), (self.frame_width -
                                                             self.frameR, self.frame_height-self.frameR), (0, 0, 255), 2)
        if hands and self.face_d:
            for hand in hands:
                # mp_hands.HAND_CONNECTIONS for lines
                if self.draw == True:
                    self.mp_drawing_utils.draw_landmarks(
                        frame, hand, self.mp_hands.HAND_CONNECTIONS)
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    handedness = str(handed)
                    cx = int(landmark.x*640)
                    cy = int(landmark.y*480)

                    hand_list.append([id, cx, cy])

                    if id == 8 and self.draw == True:
                        cv.circle(frame, center=(cx, cy),
                                  radius=7, color=(245, 39, 8), thickness=-1)
                        if (self.frameR < cx < (self.frame_width-self.frameR)) and (self.frameR < cy < (self.frame_height-self.frameR)):
                            cv.rectangle(frame, (self.frameR, self.frameR), (
                                self.frame_width - self.frameR, self.frame_height-self.frameR), (255, 0, 255), 2)
                    if click_r:
                        if id == 16:
                            cv.line(
                                frame, hand_list[8][1:], hand_list[16][1:], (0, 255, 0), 5)
                    if click_i:
                        if id == 8:
                            cv.circle(frame, (cx, cy), 7,
                                      (0, 255, 0), thickness=-1)

                    if (len(hand_list) == 21) and self.draw == True and "Right" in handedness:
                        for i in range(21):
                            xList.append(hand_list[i][1])
                            yList.append(hand_list[i][2])
                        cv.rectangle(frame, (min(xList)-20, min(yList)-20),
                                     (max(xList)+20, max(yList)+20), (0, 255, 0), 3)
                    elif (len(hand_list) == 21) and self.draw == True and "Left" in handedness:
                        for i in range(21):
                            xList.append(hand_list[i][1])
                            yList.append(hand_list[i][2])
                        cv.rectangle(frame, (min(xList)-20, min(yList)-20),
                                     (max(xList)+20, max(yList)+20), (0, 255, 0), 3)
        cv.imshow('virtual mouse', frame)
        cv.waitKey(1)
        self.face_d = False
        return frame, hand_list

    def distance(self, x1, y1, x2, y2):
        #length = math.hypot(x1, y1, x2, y2)
        length = math.sqrt((x2-x1)**2+(y2-y1)**2)
        return length

    def selfie(self, img):
        cv.imwrite('selfie'+str(self.i)+'.png', img)
        self.i += 1

    '''def drawOnImage(self, sig):
        self.draw = sig
'''


def fingerUp(hand_list, finger_tips):
    fingers = []
    land_mks = hand_list

    if len(land_mks) != 0:
        if land_mks[finger_tips[0]][1] < land_mks[finger_tips[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            if land_mks[finger_tips[id]][2] < land_mks[finger_tips[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
    return fingers


# if __name__ == "__main__":
'''
h = HandLandmarks()
while True:
    h.handDetector()

capture.release()
'''
