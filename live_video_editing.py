import numpy as np
import cv2 as cv

from numpy.random import randint

def draw_rectangle(image):
    cv.rectangle(image, (200, 200), (500, 500), (255,105,180), 500)

video_path = 'live_videos/HCS/HCS_Main_Video.mp4'
zoomed_video_path = 'live_videos/HCS/HCS Zoomed.mp4'


showZoomed = False
hovering=False


def handle_click(event, x, y, flags, param):
    global showZoomed
    global hovering

    if (x > 800 and x < 1030) and (y > 100 and y < 200):
        hovering = True

    else:
        hovering = False

    if event == cv.EVENT_LBUTTONDOWN and hovering:
        showZoomed = not showZoomed

    return

cv.namedWindow('HCS')
cv.setMouseCallback('HCS',handle_click)

height=1000
width=500

cap_main = cv.VideoCapture(video_path)
cap_zoomed = cv.VideoCapture(zoomed_video_path)

while cap_main.isOpened():
    ret, frame = cap_main.read()
    ret_z, frame_zoomed = cap_zoomed.read()


    if showZoomed:
       cv.namedWindow('HCS Zoomed')
       frame_zoomed = cv.resize(frame_zoomed, (500, 500))
       cv.imshow('HCS Zoomed', frame_zoomed)

    if not showZoomed and cv.getWindowProperty('HCS Zoomed',cv.WND_PROP_VISIBLE):
        cv.destroyWindow('HCS Zoomed')

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame = cv.resize(frame,(1500,800))

    cv.imshow('HCS',frame)
    buttonText = cv.putText(frame, 'Zoom in', (850,150), cv.FONT_HERSHEY_SIMPLEX,
                        1, (10,20,20), 2, cv.LINE_AA)


    if not hovering:
        cv.rectangle(frame, (1050, 150), (1280, 250), (255,0,0), 100)
    else:
        cv.rectangle(frame, (1050, 150), (1280, 250), (200, 0, 0), 100)
    cv.imshow('HCS',buttonText)

    if cv.waitKey(1) == ord('q'):
        break

cap_main.release()
cv.destroyAllWindows()
