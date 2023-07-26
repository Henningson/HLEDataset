import cv2
import json
import numpy as np

import os
import sys

def draw_laserdots(image, dots, seg):
    seg = glottal_segmentations[frame_num]
        
    for i in range(dots.shape[0]):
        if np.isnan(dots[i]).any():
            continue

        if cv2.pointPolygonTest(np.expand_dims(np.array(seg), 1).astype(np.uint), dots[i], False) < 0:
            cv2.circle(image, dots[i].astype(np.int), radius=2, thickness=-1, color=255)


def draw_segmentation(image, segmentation):
    cv2.fillPoly(image, np.expand_dims(np.array(segmentation, dtype=np.int32), 0), color=(255, 255, 255))

def draw_midlines(image, line):
    cv2.line(image, line[0].astype(np.int), line[1].astype(np.int), color=(255, 0, 0), thickness=2)


def write_laserdot_mask(key, index, mask_image):
    path = "dataset/" + key + "/mask/"

    try:
        os.mkdir(path)
    except:
        pass

    cv2.imwrite("{}{:05d}.png".format(path, index), mask_image)

def write_image(key, index, image):
    path = "dataset/" + key + "/png/"
    try:
        os.mkdir(path)
    except:
        pass

    cv2.imwrite("{}{:05d}.png".format(path, index), image)

def write_glottal_segmentation(key, index, image):
    path = "dataset/" + key + "/glottal_mask/"
    try:
        os.mkdir(path)
    except:
        pass

    cv2.imwrite("{}{:05d}.png".format(path, index), image)



if __name__ == "__main__":
    # Open File
    name = sys.argv[-1] if len(sys.argv[-1]) == 2 else "CM"

    with open("dataset/{0}/{0}.json".format(name)) as file:
        # Load JSON File
        DICT = json.load(file)

    cap = cv2.VideoCapture('dataset/{0}/{0}.avi'.format(name))

    #Printing available keys
    print(DICT.keys())

    # Extract glottal midlines, segmentations and laserdots
    glottal_segmentations = DICT["GlottalSegmentation"]
    #glottal_midlines = np.array(DICT["GlottalMidline"])
    #laserdots_2d = np.array(DICT["2DPoints"])

    # Transforming from FRAME_NUM x X x Y x 2 to FRAME_NUM x X*Y x 2
    #laserdots_2d = laserdots_2d.reshape(laserdots_2d.shape[0], -1, 2)

    frame_num = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        
        if not ret:
            break
        
        try:
            black_bg = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
            #draw_laserdots(black_bg, laserdots_2d[frame_num], glottal_segmentations[frame_num])
            draw_segmentation(black_bg, glottal_segmentations[frame_num])
            #write_laserdot_mask(name, frame_num, black_bg)
            #write_image(name, frame_num, frame)
            write_glottal_segmentation(name, frame_num, black_bg)
            frame_num += 1
        except:
            break