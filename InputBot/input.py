import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from mss import MSS as mss
import chess
from numpy.ma.core import sort


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

PIECES_NAMES = {
    "pawn": "p",
    "rook": "r",
    "knight": "n",
    "bishop": "b",
    "queen": "q",
    "king": "k"
}

folder = "InputBot/ressources/pieces"

board = {
  'wr': ['a1', 'h1'],
  'wn': ['b1', 'g1'],
  'wb': ['c1', 'f1'],
  'wq': ['d1'],
  'wk': ['e1'],
  'wp': ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
  'bp': ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
  'br': ['a8', 'h8'],
  'bn': ['b8', 'g8'],
  'bb': ['c8', 'f8'],
  'bq': ['d8'],
  'bk': ['e8']
}


def main():
    with mss() as sct:
        region = {
            "top": 221,
            #"left": MONITOR_1 + 352,
            "left": 280,
            "width": 873,
            "height": 873,
        }

        sct_image = sct.grab(region)
        np_image = np.array(sct_image)
        """ cv2.imshow("Capture", np_image)
        cv2.waitKey(0) """


        dict_squares, drawn_img, dh, dw = match_board(np_image)

        display, matches = detect_piece(drawn_img)

        nearest_squares = get_pieces_positions(matches, dict_squares)

        print(get_move(nearest_squares, board))

        plt.figure(figsize=(10,8))
        plt.subplot(121)
        plt.imshow(cv2.cvtColor(display,cv2.COLOR_BGR2RGB))
        plt.title("Template Matching Result")
        plt.show()


def get_pieces_positions(matches, dict_squares):
    nearest_squares = {}
    for match in matches:
        x,y,_,_ = match["bbox"]
        min_dist = np.inf
        nearest_sqr = ""
        for point in dict_squares:
            d = np.sqrt((point[0] - x)**2 + (point[1] - y)**2)
            if d < min_dist:
                min_dist = d
                nearest_sqr = dict_squares[point]
        template = match["template"].removesuffix(".png")
        nearest_squares.setdefault(template, []).append(nearest_sqr)
    return nearest_squares

def get_move(nearest_squares, board):
    res = []
    diff_vals = [(nearest_squares[k], board[k]) for k in nearest_squares.keys() & board.keys() if sorted(nearest_squares[k]) != sorted(board[k])]
    if diff_vals:
        for each_diff in diff_vals:
            l1, l2 = each_diff

            only_in_l2 = [x for x in l2 if x not in l1]
            only_in_l1 = [x for x in l1 if x not in l2]

            move = only_in_l2 + only_in_l1
            print("move:", move)
            if len(move) == 1:
                continue
            previous, current = move
            res.append(previous + current)
        return res

    else:
        print("No differences found")

def draw_matches(matches,img):
    draw_img = img.copy()
    for match in matches:
        x1,y1,x2,y2 = match["bbox"]
        #drawn_img = cv2.rectangle(draw_img, (x1,y1),(x2,y2),(0,0,0),3)
        drawn_img = cv2.putText(
            img=draw_img,
            text=f"{match['template']}",
            org=(x1 + 10, y1 +50),
            fontFace=cv2.FONT_HERSHEY_COMPLEX,
            fontScale=0.75,
            color=(0,255,0),
            thickness=3
        )
    return drawn_img

def post_process_locs(points):
    kept_locs = []
    duplicates_idx =[]
    #print("Nb of points", len(points))
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


def detect_piece(img):
    if img is None:
        board = cv2.imread("InputBot/ressources/board2.png")
    else:
        board = img

    board_rgb = cv2.cvtColor(board,cv2.COLOR_BGR2RGB)
    board_gray = cv2.cvtColor(board,cv2.COLOR_BGR2GRAY)

    matches = []
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        piece = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        piece = cv2.resize(piece,(100,100))
        h,w = piece.shape

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

        y_arr,x_arr = np.where(res >= 0.92)
        points = list(zip(x_arr,y_arr))
        points = post_process_locs(points)

        for point in points:
            matches.append({
                "template": filename,
                "score": res[point[1],point[0]],
                "bbox":(point[0],point[1],point[0]+w,point[1]+h)
            })

    display = draw_matches(matches,board)

    """ plt.figure(figsize=(10,8))
    plt.subplot(121)
    plt.imshow(cv2.cvtColor(display,cv2.COLOR_BGR2RGB))
    plt.title("Template Matching Result")
    plt.show() """

    return display,matches

def draw_squares(all_squares, img, dw, dh,dict):
    draw_img = img.copy()
    for x, y in all_squares:
        cv2.rectangle(draw_img, (x, y), (x+dw, y+dh), (0, 255, 0), 2)
        cv2.putText(draw_img, dict[(x, y)], (x+5, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
    return draw_img


def match_board(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    corners = cv2.cornerHarris(gray, blockSize=4, ksize=3, k=0.04)
    y_arr, x_arr = np.where(corners > 0.001 * corners.max())
    points_w = list(zip(x_arr[:10],y_arr[:10]))
    points_w = post_process_locs(points_w)
    points_w = sorted(points_w, key=lambda p: (p[0], p[1]))
    points_h = [(x,y) for x,y in zip(x_arr,y_arr) if abs(x-points_w[0][0]) < 3]
    points_h = post_process_locs(points_h)
    points_h = sorted(points_h, key=lambda p: (p[0], p[1]))

    points = points_w + points_h

    first_point = points_w[0]

    dw = abs(first_point[0] - points_w[1][0])+2
    dh = abs(first_point[1] - points_h[0][1])+2

    all_squares = [(x,y) for x in range(first_point[0], first_point[0]+(dw*8), dw) for y in range(first_point[1], first_point[1]+(dh*8), dh)]

    labels = ["a8", "a7", "a6", "a5", "a4", "a3", "a2", "a1",
        "b8", "b7", "b6", "b5", "b4", "b3", "b2", "b1",
        "c8", "c7", "c6", "c5", "c4", "c3", "c2", "c1",
        "d8", "d7", "d6", "d5", "d4", "d3", "d2", "d1",
        "e8", "e7", "e6", "e5", "e4", "e3", "e2", "e1",
        "f8", "f7", "f6", "f5", "f4", "f3", "f2", "f1",
        "g8", "g7", "g6", "g5", "g4", "g3", "g2", "g1",
        "h8", "h7", "h6", "h5", "h4", "h3", "h2", "h1",
    ]

    dict_squares = {p: label for p, label in zip(all_squares, labels)}
    drawn_img = draw_squares(all_squares, img,dh,dw,dict_squares)
    """ plt.figure(figsize=(10,8))
    plt.subplot(121)
    plt.imshow(cv2.cvtColor(drawn_img, cv2.COLOR_BGR2RGB))
    plt.title("Template Matching Result")
    plt.show() """

    return dict_squares, drawn_img, dh,dw



if __name__ == "__main__":
    main()
