import src. imageProcess as imageProcess 
import sys,getopt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math
import os
from moviepy.editor import VideoFileClip
from IPython.display import HTML

# -v video path
# -s save path
videoPath = ''
savePath = ''
argss = sys.argv[1:]

try:
    opts, args = getopt.getopt(argss, "hv:s:", ["vpath=", "spath="])
except getopt.GetoptError:
    print('main.py -v <VideoPath> -s <SavePath>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('main.py -v <VideoPath> -s <SavePath>')
        sys.exit()
    elif opt in ("-v","--vpath"):
        videoPath=arg
    elif opt in ("-s","--spath"):
        savePath=arg

if savePath == '':
    savePath='result/'

def getVideo(path):
    cap = cv2.VideoCapture(path)
    return cap


def saveVideo(cap,spath):
    forucc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(spath,
                          forucc, 60.0, (int(cap.get(3)), int(cap.get(4))))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            # frame = cv2.flip(frame,1,dst=none) #frame cevirmek icin
            res = imageProcess.run(frame)
            out.write(res)
            cv2.imshow('result', res)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


#c = getVideo(imageProcess.set.testdeo)
print(videoPath +'\n'+savePath)
saveVideo(getVideo(videoPath),savePath)
