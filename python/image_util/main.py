#%%
import cv2
import numpy as np
from scipy.ndimage.filters import rank_filter
from typing import List, Tuple, Iterable, Callable
from pathlib import Path

from matplotlib import rcParams as mpl_param
import matplotlib.pyplot as plt

mpl_param["figure.dpi"] = 200

IMAGE_WORD_SIZE_GAP = {
    "x": 3,
    "y": 9,
}


#%%
def sort_contours(
    contours: Iterable[np.ndarray], method: str = "top-to-bottom"
) -> Tuple[Iterable[np.ndarray], Iterable]:
    boundingBoxes = []
    reverse = False
    i = 0

    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of b_boxes and sort from top to bottom
    if contours:
        boundingBoxes = [cv2.boundingRect(c) for c in contours]
        (contours, boundingBoxes) = zip(
            *sorted(
                zip(contours, boundingBoxes), key=lambda b: b[1][i], reverse=reverse
            )
        )

    return contours, boundingBoxes


def get_rects_from_contours(contours):
    MIN_HEIGHT = 10
    MIN_LINE_GAP = -4
    ret_rects = []
    # Sorting contours from top to bottom
    contours, __ = sort_contours(contours)
    for contour in contours:
        # epsilon = 0.05*cv2.arcLength(contour, True)
        # approx = cv2.approxPolyDP(contour, epsilon, True)
        # (x, y, w, h) = cv2.boundingRect(approx)
        (x, y, w, h) = cv2.boundingRect(contour)
        if h < MIN_HEIGHT:
            continue
        if ret_rects and y - ret_rects[-1][3] < MIN_LINE_GAP:
            ret_rects[-1][0] = min(ret_rects[-1][0], x)
            ret_rects[-1][1] = min(ret_rects[-1][1], y)
            ret_rects[-1][2] = max(ret_rects[-1][2], x + w)
            ret_rects[-1][3] = max(ret_rects[-1][3], y + h)
        else:
            ret_rects.append([x, y, x + w, y + h])
    return ret_rects


#%%
def separate_img_line(img: np.ndarray) -> np.ndarray:
    """Insert Vertical line between 2 row, which have delta of 2 row value mean > 25"""
    NUM_LINE_ADDED = 1

    line = np.zeros((1, img.shape[1]), dtype=np.uint8)
    for idx, row in enumerate(img):
        mean = np.mean(row)
        if (
            mean < 100
            and 0 < idx < len(img) - NUM_LINE_ADDED + 1
            and np.mean(img[idx - 1]) > 0
            and abs(np.mean(img[idx - 1]) - mean) > 25
        ):
            for i in range(NUM_LINE_ADDED):
                img[idx + i] = line

    return img


CONTOUR_VALIDATOR = Callable[[np.ndarray], bool]


def detect_contours(
    img: np.ndarray,
    hier_option,
    contour_validator: CONTOUR_VALIDATOR = lambda x: cv2.contourArea(x) > 750,
) -> List[np.ndarray]:
    """cv2.findContours with some options on hier and rect detected

    Note:
        OpenCV Hierarchy use format as [Next idx, Previous idx, First_Child idx, Parent idx]
        with `-1` is Not exist

    Args:
        img (np.ndarray): Input image to findContours
        hier_option (Literal["most-outer", "most-inner", "all"]): Hier. Option for contours filter
        contour_validator (CONTOUR_VALIDATOR, optional): Contours size filter. Defaults to lambda x: cv2.contourArea(x) > 750.

    Raises:
        ValueError: when `hier_option` not in `["most-outer", "most-inner", "all"]`

    Returns:
        List[np.ndarray]: List of valid contours
    """
    cnts, hiers = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    back_ground_cnts = []

    hier_validator: CONTOUR_VALIDATOR = lambda h: False
    if hier_option == "most-outer":
        hier_validator: CONTOUR_VALIDATOR = lambda h: h[3] == -1
    elif hier_option == "most-inner":
        hier_validator: CONTOUR_VALIDATOR = lambda h: h[2] == -1
    elif hier_option == "all":
        hier_validator: CONTOUR_VALIDATOR = lambda h: True
    else:
        raise ValueError("Wrong `detect_contours` kwargs `hier_option`")

    for idx, cnt in enumerate(cnts):
        rect_cnt = np.int0(cv2.boxPoints(cv2.minAreaRect(cnt)))
        if hier_validator(hiers[0][idx]) and contour_validator(rect_cnt):
            back_ground_cnts.append(rect_cnt)

    return back_ground_cnts


def _contour_validator(cnt: np.ndarray) -> bool:
    """Contour Validator for `detect_most_cnt_cover` func.

    Args:
        cnt (np.ndarray): numpy array of contour poins

    Returns:
        [bool]: Valid of not?
    """
    x, y, w, h = cv2.boundingRect(cnt)
    return (
        w > 15
        and h > IMAGE_WORD_SIZE_GAP["y"]
        and w * h > 15 * IMAGE_WORD_SIZE_GAP["y"] * 2
    )


# %%
sample_results = []
for sample in Path("./data/input").glob("*.png"):
    sample_results.append((str(sample.absolute()), int(sample.stem.split("_")[-1])))

#%%
chosen_sample = 6

gray = cv2.imread(sample_results[chosen_sample][0])
gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
plt.imshow(gray)

#%%
edges = cv2.Canny(gray, 100, 200)
# plt.imshow(edges)

# Remove ~1px borders using a rank filter.
maxed_rows = rank_filter(edges, -4, size=(1, 20))
debordered = np.minimum(gray, maxed_rows)
# plt.imshow(debordered)

# 1st Try: Dilating and erosing with Horizontal kernel
N = 15
kernel = np.zeros((N, N), dtype=np.uint8)
kernel[(N - 1) // 2, :] = 1

dilated_image = cv2.dilate(debordered, kernel, iterations=3)
# plt.imshow(dilated_image)

eroded_image = cv2.erode(dilated_image, kernel, iterations=3)
# plt.imshow(eroded_image)

# 2nd Try: Dilating and erosing with Vertical kernel
N = 2
kernel = np.zeros((N, N), dtype=np.uint8)
kernel[:, (N - 1) // 2] = 1

dilated_image = cv2.dilate(eroded_image, kernel, iterations=1)
# plt.imshow(dilated_image)

eroded_image = cv2.erode(dilated_image, kernel, iterations=1)
eroded_image = eroded_image.astype(np.uint8)
plt.imshow(eroded_image)

# Seperating Image text line based row pixel mean
separateed_image = separate_img_line(eroded_image)
plt.imshow(separateed_image)


#%%
# Detect seperated contour cover text-lines
cnts = detect_contours(
    separateed_image, hier_option="all", contour_validator=_contour_validator
)
print(len(cnts))
# cnts, hiers = cv2.findContours(separateed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
mask = np.zeros_like(separateed_image)
cv2.drawContours(mask, cnts, -1, 255, -1)
plt.imshow(mask)

# show_cnt_with_idx(cnts)

assert (
    len(cnts) >= sample_results[chosen_sample][1]
), f"Mis-match: CHOSEN ONLY {len(cnts)}, INSTEAD of {sample_results[chosen_sample][1]} result"

# mask = np.zeros_like(separateed_image)
# cv2.drawContours(mask, cnts, -1, 255, -1)
# plt.imshow(mask)


#%%

# Find contours and their bounding boxes
# contours, _ = cv2.findContours(eroded_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# line_bounding_rects = get_rects_from_contours(contours)
# line_bounding_rects

#%%

# # For debugging
def show_cnt_with_idx(cnts):
    blank_image = 0 * np.ones(gray.shape, dtype="uint8")
    for idx, cnt in enumerate(cnts):
        x0, y0, w, h = cv2.boundingRect(cnt)
        x1 = x0 + w
        y1 = y0 + h
        cv2.rectangle(blank_image, (x0, y0), (x1, y1), (255, 255, 255), 2)
        cv2.putText(
            blank_image,
            str(idx),
            (x1, y1),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            lineType=cv2.LINE_AA,
        )

    plt.imshow(blank_image)


# %%
ord("�")
# %%
temp_a = {"12345": 1, "09876": 2}
temp_b = {"09876": 2, "12345": 1}

list_temp = [1,2,3,4,5,67,76,7,34,634,.76,8,]
for i in range(10):
    print(id(list_temp))
    print(id(sorted(list_temp)))
    print(id(list(list_temp)))
    print("\n")

# %%
max(dict([("a", 1), ("a", 2)]).values())
# %%
sorted([], key=lambda s: s["y1"])
# %%
set_a = set([1,2,3])
1 in set_a
# %%
