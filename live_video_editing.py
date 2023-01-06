import numpy as np
import cv2 as cv

from numpy.random import randint

def draw_rectangle(image,x1,y1,x2,y2,color,thickness):
    cv.rectangle(image, (x1, y1), (x2, y2), color, thickness)

video_path = 'live_videos/HCS/HCS_Main_Video.mp4'
zoomed_video_path = 'live_videos/HCS/HCS Zoomed.mp4'
zoomed_graph_path = 'live_videos/HCS/HCS Graphic.mp4'


showZoomed = False
showZoomedGraph = False

hoveringZoomTest = False
hoveringZoomGraph = False

def handle_click(event, x, y, flags, param):
    global showZoomed
    global hoveringZoomTest
    global hoveringZoomGraph
    global showZoomedGraph

    if (x > 0 and x < 300) and (y > 0 and y < 85):
        hoveringZoomTest = True
    else:
        hoveringZoomTest = False

    if (x > 0 and x < 300) and (y > 140 and y < 225):
        hoveringZoomGraph = True

    else:
        hoveringZoomGraph = False

    if event == cv.EVENT_LBUTTONDOWN and hoveringZoomTest:
        showZoomed = not showZoomed

    if event == cv.EVENT_LBUTTONDOWN and hoveringZoomGraph:
        showZoomedGraph = not showZoomedGraph

    return

cv.namedWindow('HCS')
cv.setMouseCallback('HCS',handle_click)

height=1000
width=500

cap_main = cv.VideoCapture(video_path)
cap_zoomed = cv.VideoCapture(zoomed_video_path)
cap_zoomed_graph = cv.VideoCapture(zoomed_graph_path)

while cap_main.isOpened():
    ret, frame = cap_main.read()
    ret_z, frame_zoomed = cap_zoomed.read()
    ret_z_g,frame_z_g = cap_zoomed_graph.read()

    if showZoomed:
       cv.namedWindow('HCS Zoomed')
       frame_zoomed = cv.resize(frame_zoomed, (500, 500))
       cv.imshow('HCS Zoomed', frame_zoomed)

    if not showZoomed and cv.getWindowProperty('HCS Zoomed',cv.WND_PROP_VISIBLE):
        cv.destroyWindow('HCS Zoomed')



    if showZoomedGraph:
        cv.namedWindow('HCS Zoomed Graph')
        frame_z_g = cv.resize(frame_z_g,(500,500))
        cv.imshow('HCS Zoomed Graph',frame_z_g)

    if not showZoomedGraph and cv.getWindowProperty('HCS Zoomed Graph',cv.WND_PROP_VISIBLE):
        cv.destroyWindow('HCS Zoomed Graph')


    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    if not hoveringZoomTest:
        draw_rectangle(frame,0,0,100,10,(255,0,0),50)
    else:
        draw_rectangle(frame,0,0,100,10,(200,0,0),50)


    if not hoveringZoomGraph:
        draw_rectangle(frame,0,75,100,85,(255,0,0),25)
    else:
        draw_rectangle(frame,0,75,100,85,(200,0,0),25)

    fontScale = 0.9
    font = cv.FONT_HERSHEY_SIMPLEX
    thickness = 2
    color = (0,0,0)

    frame = cv.resize(frame,(1500,800))

    cv.imshow('HCS',frame)

    if not showZoomed:
        zoomInTest = cv.putText(frame, 'Zoom in(Instron)', (5,50), font,
                   fontScale, color, thickness, cv.LINE_AA)
        cv.imshow('HCS',zoomInTest)

    else:
        zoomOutTest = cv.putText(frame, 'Zoom Out(Instron)', (5,50), font,
                   fontScale, color, thickness, cv.LINE_AA)
        cv.imshow('HCS',zoomOutTest)

    if not showZoomedGraph:
        zoomInGraph = cv.putText(frame, 'Zoom in(Graph)', (5,200), font,
                   fontScale, color, thickness, cv.LINE_AA)
        cv.imshow('HCS',zoomInGraph)
    else:
        zoomInGraph = cv.putText(frame, 'Zoom out(Graph)', (5,200), font,
                   fontScale, color, thickness, cv.LINE_AA)
        cv.imshow('HCS',zoomInGraph)


    if cv.waitKey(1) == ord('q'):
        break

cap_main.release()
cv.destroyAllWindows()
