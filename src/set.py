import numpy as np

jpg = '.jpg'
png = '.png'
mp4 = '.mp4'
avi = '.avi'
imagesPath = 'images/'
resultImagesPath = imagesPath+'res/'
testImage = imagesPath+'test1'+jpg
resultImagesName = 'result_'
low_threshold = 50
high_threshold = 150
kernel_size = 5
threshold = 20
rho = 2
theta = np.pi/180
min_line_len = 50
max_line_gap = 200
α = 0.8
β = 1.
λ = 0.
videoPath = 'videos/'
testVideo = videoPath+'test'+mp4
