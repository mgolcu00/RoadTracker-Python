# usage : command panel ->
# python main.py -v <VideoPath> -s <SavePath>
# VideoPath = the name or path of the mp4 video file you want to use / kullanmak istediğiniz mp4 video dosyasının adı yada yolu
# SavePath = file name and path where the processed and drawn path video will be saved / işlenen ve çizilen yol videosunun kaydedileceği dosya ismi ve yolu
#
# tr / örnek kullanım şekli -> python main.py -v videos/test.mp4 -s result/result.mp4
#

import src.still_processing as sp
import src.imageProcess as imageProcess
import src.line_detector as ld
import sys
import getopt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math
import os

# -v video path
# -s save path
videoPath = ''
savePath = ''
mode = ''
argss = sys.argv[1:]

try:
    opts, args = getopt.getopt(argss, "hv:s:m:", ["vpath=", "spath=", "mode="])
except getopt.GetoptError:
    print('main.py -v <VideoPath> -s <SavePath> -m <mode>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('main.py -v <VideoPath> -s <SavePath> -m <mode>')
        sys.exit()
    elif opt in ("-v", "--vpath"):
        videoPath = arg
    elif opt in ("-s", "--spath"):
        savePath = arg
    elif opt in ("-m", "--mode"):
        mode = arg

if savePath == '':
    savePath = 'result/'


def getVideo(path):
    cap = cv2.VideoCapture(path)
    return cap


def saveVideo(cap, spath):
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


def saveVideo2(cap, spath):
    forucc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(spath,
                          forucc, 60.0, (int(cap.get(3)), int(cap.get(4))))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            # frame = cv2.flip(frame,1,dst=none) #frame cevirmek icin
            res = sp.process_image(frame)
            out.write(res)
            cv2.imshow('result', res)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def saveVideo3(cap, spath):
    forucc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(spath,
                          forucc, 60.0, (int(cap.get(3)), int(cap.get(4))))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            # frame = cv2.flip(frame,1,dst=none) #frame cevirmek icin
            res = ld.find_street_lanes(frame)
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
# print(videoPath + '\n'+savePath)
# print(mode)

vid = getVideo(videoPath)


if mode == '1':
    saveVideo(vid, savePath)
elif mode == '2':
    saveVideo2(vid, savePath)
else:
    print('mode error try (1 or 2)')
