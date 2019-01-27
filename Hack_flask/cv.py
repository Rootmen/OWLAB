import time

import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

BLUR = 21
CANNY_THRESH_1 = 10
CANNY_THRESH_2 = 200
MASK_DILATE_ITER = 10
MASK_ERODE_ITER = 10
MASK_COLOR = (0.0, 0.0, 1.0)  # In BGR format


def imagecup(imgo):
    height, width = imgo.shape[:2]
    # Create a mask holder
    mask = np.zeros(imgo.shape[:2], np.uint8)

    # Grab Cut the object
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # Hard Coding the Rect The object must lie within this rect.
    rect = (10, 10, width - 30, height - 30)
    cv2.grabCut(imgo, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img1 = imgo * mask[:, :, np.newaxis]

    # Get the background
    background = imgo - img1

    # Change all pixels in the background that are not black to white
    background[np.where((background > [0, 0, 0]).all(axis=2))] = [255, 255, 255]

    # Add the background and the image
    final = background + img1

    # To be done - Smoothening the edges
    return final


def imagecup2(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # -- Edge detection -------------------------------------------------------------------
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    # -- Find contours in edges, sort by area ---------------------------------------------
    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    # -- Create empty mask, draw filled polygon on it corresponding to largest contour ----
    # Mask is black, polygon is white
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    # -- Smooth mask, then blur it --------------------------------------------------------
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask] * 3)  # Create 3-channel alpha mask

    # -- Blend masked img into MASK_COLOR background --------------------------------------
    mask_stack = mask_stack.astype('float32') / 255.0  # Use float matrices,
    img = img.astype('float32') / 255.0  # for easy blending

    masked = (mask_stack * img) + ((1 - mask_stack) * MASK_COLOR)  # Blend
    masked = (masked * 255).astype('uint8')  # Convert back to 8-bit
    return masked


def cupany():
    """Merge two images into one, displayed side by side
    :param file1: path to first image file
    :param file2: path to second image file
    :return: the merged Image object
    """
    image1 = Image.open("/home/rootmen/Git/Hack_flask/templates/rez1.jpg")
    image2 = Image.open("/home/rootmen/Git/Hack_flask/templates/rez2.jpg")
    image3 = Image.open("/home/rootmen/Git/Hack_flask/templates/rez3.jpg")
    image4 = Image.open("/home/rootmen/Git/Hack_flask/templates/rez4.jpg")
    (width1, height1) = image1.size
    (width2, height2) = image2.size
    (width3, height3) = image3.size
    (width4, height4) = image4.size
    result_width = width1 + width2
    result_height = height1 + height2
    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))
    result.paste(im=image3, box=(0, height1))
    result.paste(im=image4, box=(width1, height1))
    result.save("/home/rootmen/Git/Hack_flask/templates/good.jpg")
    s_img = cv2.imread("/home/rootmen/Git/Hack_flask/templates/good.jpg", -1)

    return


def cuppatch(patch):
    img = cv2.imread(patch)
    img = imagecup2(imagecup(img))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('rez' + patch + ".jpg", gray)


def blend_transparent():
    img = Image.open('/home/rootmen/Git/Hack_flask/templates/good.jpg')
    watermark = Image.open('/home/rootmen/Git/Hack_flask/templates/ramka.png')
    img.paste(watermark, (10, 10), watermark)
    img.save("/home/rootmen/Git/Hack_flask/templates/img_with_watermark.png")


def maincv():
    blend_transparent()
    # Load the Image
    # img = cv2.imread('5.jpg')
    start_time = time.time()
    cuppatch("/home/rootmen/Git/Hack_flask/templates/1")
    cuppatch("/home/rootmen/Git/Hack_flask/templates/2")
    cuppatch("/home/rootmen/Git/Hack_flask/templates/3")
    cuppatch("/home/rootmen/Git/Hack_flask/templates/4")
    cupany()
    blend_transparent()
    print("--- %s seconds ---" % (time.time() - start_time))
