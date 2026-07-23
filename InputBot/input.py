import cv2
import numpy as np
from matplotlib import pyplot as plt
from mss import MSS as mss

MONITOR_2 = 1920
MONITOR_1 = 0


def main():
    with mss() as sct:
        region = {
            "top": 121,
            "left": MONITOR_2 + 352,
            "width": 813,
            "height": 813,
        }

        sct_image = sct.grab(region)
        np_image = np.array(sct_image)
        np_image_rgb = np_image[:, :, :3][:, :, ::-1]
        np_image_gray = np_image_rgb[:, :, 1]
        cv2.imshow("Capture", np_image_gray)
        cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
