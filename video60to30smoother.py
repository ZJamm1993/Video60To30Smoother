print 'hello'

from cv2 import cv2
import numpy as np
import time

cap = cv2.VideoCapture('test60.mp4')

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
framecount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print 'total frame: ' + str(framecount)

cc = cv2.VideoWriter_fourcc(*'X264')
savefilename = 'out30_' + time.strftime('%Y%m%d_%H%M%S') + '.mp4'
out = cv2.VideoWriter(savefilename,cc,30,(int(width),int(height)))

using3frame = '3'
using2frame = '2'
option = using2frame

frameHead = None
frameMidd = None
frameTail = None
currentframeindex = 0
while cap.isOpened():
    ret, frame = cap.read()
    if ret == False:
        break
    
    if option == using3frame:
        frameHead = frameMidd
        frameMidd = frameTail
        frameTail = frame
        if currentframeindex % 2 == 0 and currentframeindex > 0:
            firstAlpha = 0.8
            newFrame = None
            if frameHead.any() :
                newFrame = cv2.addWeighted(frameHead, firstAlpha, frameTail,1-firstAlpha,0)
            else :
                newFrame = frameTail
            firstAlpha = 0.2
            newFrame = cv2.addWeighted(frameMidd, firstAlpha,newFrame,1-firstAlpha,0)
            # create a new frame with 3 old frames
            # how to make it smoother??
            out.write(newFrame)

    elif option == using2frame:
        if currentframeindex % 2 == 0:
            frameMain = frame
        else :
            firstAlpha = 0.7
            # frame = cv2.addWeighted(frameMain,firstAlpha,frame,1-firstAlpha,0)
            newFrame = np.zeros((height, width,3),np.uint8)
            for i in range(height):
                if i % 2 == 0:
                    newFrame[i] = frameMain[i]
                else :
                    newFrame[i] = frame[i]
                    
            # create a new frame with 2 old frams
            # cv2.imshow('1', newFrame)
            # cv2.waitKey(0)
            out.write(newFrame)

    # print and loop
    print 'progress:'+str(currentframeindex)+'/'+str(framecount)
    currentframeindex += 1
    
cap.release()
out.release()
print 'finish'
# cv2.destroyAllWindows()