

from multiprocessing.reduction import duplicate

import cv2
import numpy as np
from matplotlib import pyplot as plt
from mss import MSS as mss

MONITOR_2 = 1920
MONITOR_1 = 0

METHODS = {
    "TM_SQDIFF",
    "TM_SQDIFF_NORMED",
    "TM_CCORR",
    "TM_CCORR_NORMED",
    "TM_CCOEFF",
    "TM_CCOEFF_NORMED"
}

def main():
    '''
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
    '''
    detect_piece()

def draw_matches(matches,img):
    draw_img = img.copy()
    for match in matches:
        x1,y1,x2,y2 = match["bbox"]
        drawn_img = cv2.rectangle(draw_img, (x1,y1),(x2,y2),(0,0,0),3)
        drawn_img = cv2.putText(
            img=drawn_img,
            text=f"{match['template']}: {match['score']:.2f}",
            org=(x1 - 5, y1 -10),
            fontFace=cv2.FONT_HERSHEY_COMPLEX,
            fontScale=0.5,
            color=(0,0,0),
            thickness=3
        )
    return drawn_img

def post_process_locs(points):
    kept_locs = []
    duplicates_idx =[]
    print("Nb of points", len(points))
    for idx1 in range(len(points) -1):
        x1,y1 = points[idx1]
        for idx2 in range(idx1+1,len(points)):
            if idx2 in duplicates_idx:
                continue
            x2,y2 = points[idx2]
            if abs(x1-x2) < 5 and abs(y1-y2) <5:
                duplicates_idx.append(idx2)
    for idx in range(len(points)):
        if idx not in duplicates_idx:
            kept_locs.append(points[idx])
    return kept_locs


def detect_piece():

    board = cv2.imread("InputBot/ressources/board.png")
    board_rgb = cv2.cvtColor(board,cv2.COLOR_BGR2RGB)
    board_gray = cv2.cvtColor(board,cv2.COLOR_BGR2GRAY)

    piece = cv2.imread("InputBot/ressources/bb.png", cv2.IMREAD_GRAYSCALE)
    piece = cv2.resize(piece,(100,100))
    h,w = piece.shape

    matches = []
    method = "TM_CCORR_NORMED"
    cv2_method = getattr(cv2,method)
    res = cv2.matchTemplate(board_gray,piece,cv2_method)
    """ min_val, max_val, min_loc,max_loc = cv2.minMaxLoc(res)
        if cv2_method in [cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED]:
            point = min_loc
            score = min_val
        else:
            point = max_loc
            score = max_val """

    y_arr,x_arr = np.where(res >= 0.95)
    points = list(zip(x_arr,y_arr))
    points = post_process_locs(points)

    for point in points:
        matches.append({
            "template": "black bishop",
            "score": res[point[1],point[0]],
            "bbox":(point[0],point[1],point[0]+w,point[1]+h)
        })

    display = draw_matches(matches,board)

    plt.figure(figsize=(10,8))
    plt.subplot(121)
    plt.imshow(cv2.cvtColor(display,cv2.COLOR_BGR2RGB))
    plt.title(f"Template Matching Result: {method}")

    plt.subplot(122)
    plt.imshow(res, cmap="gray")
    plt.title(f"Match scores {method}")
    plt.show()




if __name__ == "__main__":
    main()
