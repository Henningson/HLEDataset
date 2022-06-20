import cv2
import json
import numpy as np

def draw_laserdots(image, dots):
    for i in range(dots.shape[0]):
        if np.isnan(dots[i]).any():
            continue

        cv2.circle(image, dots[i].astype(np.int), radius=2, thickness=-1, color=(0, 255, 0))


def draw_segmentation(image, segmentation):
    cv2.fillPoly(image, np.expand_dims(np.array(segmentation, dtype=np.int32), 0), color=(255, 255, 255))

def draw_midlines(image, line):
    cv2.line(image, line[0].astype(np.int), line[1].astype(np.int), color=(255, 0, 0), thickness=2)


if __name__ == "__main__":
    # Open File
    with open("dataset/CM/CM.json") as file:
        # Load JSON File
        CM_DICT = json.load(file)

    cap = cv2.VideoCapture('dataset/CM/CM.avi')

    #Printing available keys
    print(CM_DICT.keys())

    # Extract glottal midlines, segmentations and laserdots
    glottal_segmentations = np.array(CM_DICT["GlottalSegmentation"])
    glottal_midlines = np.array(CM_DICT["GlottalMidline"])
    laserdots_2d = np.array(CM_DICT["2DPoints"])

    # Transforming from FRAME_NUM x X x Y x 2 to FRAME_NUM x X*Y x 2
    laserdots_2d = laserdots_2d.reshape(laserdots_2d.shape[0], -1, 2)

    frame_num = 0
    while (cap.isOpened()):
        ret, frame = cap.read()

        draw_laserdots(frame, laserdots_2d[frame_num])
        draw_segmentation(frame, glottal_segmentations[frame_num])
        draw_midlines(frame, glottal_midlines[frame_num])

        cv2.imshow("CM", frame)
        cv2.waitKey(0)

        frame_num += 1
