import src.set as set
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math
import os


def getImage(path):
    return cv2.imread(path)


def getGrayImage(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def showImage(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def getMaskImage(img, vert):
    mask = np.zeros_like(img)

    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    cv2.fillPoly(mask, vert, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    try:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(img, (x1, y1), (x2, y2), color, thickness)
    except  :
        print('no line founded')


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array(
        []), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img


def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    return cv2.addWeighted(initial_img, α, img, β, λ)


def run(image):
    gray_image = getGrayImage(image)
    img_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    lower_yellow = np.array([20, 100, 100], dtype="uint8")
    upper_yellow = np.array([30, 255, 255], dtype="uint8")

    mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
    mask_white = cv2.inRange(gray_image, 200, 255)
    mask_yw = cv2.bitwise_or(mask_white, mask_yellow)
    mask_yw_image = cv2.bitwise_and(gray_image, mask_yw)

    gauss_gray = gaussian_blur(mask_yw_image, set.kernel_size)
    canny_edges = canny(gauss_gray, set.low_threshold, set.high_threshold)

    imshape = image.shape
    lower_left = [imshape[1]/9, imshape[0]]
    lower_right = [imshape[1]-imshape[1]/9, imshape[0]]
    top_left = [imshape[1]/2-imshape[1]/8, imshape[0]/2+imshape[0]/10]
    top_right = [imshape[1]/2+imshape[1]/8, imshape[0]/2+imshape[0]/10]
    vertices = [np.array([lower_left, top_left, top_right,
                          lower_right], dtype=np.int32)]
    roi_image = getMaskImage(canny_edges, vertices)

    # rho = 2  # Ro and teta are the distance and angular solution
    # theta = np.pi/180

    line_image = hough_lines(roi_image, set.rho, set.theta,
                             set.threshold, set.min_line_len, set.max_line_gap)
    result = weighted_img(line_image, image, α=0.8, β=1., λ=0.)
    return result


def saveImages():
    for source_img in os.listdir(set.imagesPath):
        image = mpimg.imread(set.imagesPath+source_img)
        processed = run(image)
        mpimg.imsave(set.imagesPath + set.resultImagesName +
                     source_img, processed)


# img = getImage(set.testImage)
# showImage(run(img))
