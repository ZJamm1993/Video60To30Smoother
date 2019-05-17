print 'hello'

from cv2 import cv2
import time

cap = cv2.VideoCapture('test60.mp4')

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
framecount = cap.get(cv2.CAP_PROP_FRAME_COUNT)

print 'total frame: ' + str(framecount)

cc = cv2.VideoWriter_fourcc(*'X264')
savefilename = 'out30_' + time.strftime('%Y%m%d_%H%M%S') + '.mp4'
out = cv2.VideoWriter(savefilename,cc,30,(int(width),int(height)))

frameHead = None
frameMidd = None
frameTail = None
tag = 0
currentframeindex = 0
while cap.isOpened():
    ret, frame = cap.read()
    if ret == False:
        break
    frameHead = frameMidd
    frameMidd = frameTail
    frameTail = frame
    if currentframeindex % 2 == 0 and currentframeindex > 0:
        firstAlpha = 0.5
        newFrame = None
        if frameHead.any() :
            newFrame = cv2.addWeighted(frameHead, firstAlpha, frameTail,1-firstAlpha,0)
        else :
            newFrame = frameTail
        firstAlpha = 0.7
        newFrame = cv2.addWeighted(frameMidd,firstAlpha,newFrame,1-firstAlpha,0)
        # create a new frame with 3 old frames

        # how to make it smoother??

        # cv2.imshow('frame',frame)
        out.write(newFrame)
        if currentframeindex % 10 == 0:
            print 'progress:'+str(currentframeindex)+'/'+str(framecount)
    currentframeindex += 1
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
cap.release()
out.release()
print 'finish'
# cv2.destroyAllWindows()