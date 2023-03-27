import cv2
import os

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

#path = '/Users/mac/Downloads/unsplashImgs/wes-hicks-ZlsdPyEcPcU-unsplash.jpg'
#imgSize = cv2.imread(path,cv2.IMREAD_UNCHANGED)
#print('dims:',imgSize.shape)
#directory = '/Users/mac/Downloads/open_cvTest'
#resized = image_resize(imgSize,width=1200)
#rszdFile = 'rszd.jpg'
#os.chdir(directory)
#cv2.imwrite(rszdFile,resized)
#print('dims:',resized.shape)

