from copy import deepcopy
from typing import List, Optional, Tuple, Iterable

import cv2
import numpy as np
from scipy.ndimage.filters import rank_filter


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


def get_line_bounding_rects(image: np.ndarray, name: Optional[str] = None):
    """returns list of (x0, y0, x1, y1)"""
    gray = deepcopy(image)
    if name:
        cv2.imwrite(f"./img_temp/{name}_1_gray.png", gray)

    edges = cv2.Canny(gray, 100, 200)
    if name:
        cv2.imwrite(f"./img_temp/{name}_2_edges.png", edges)
    
    # Remove ~1px borders using a rank filter.
    maxed_rows = rank_filter(edges, -4, size=(1, 20))
    debordered = np.minimum(gray, maxed_rows)
    if name:
        cv2.imwrite(f"./img_temp/{name}_3_debordered.png", debordered)

    # Dilating and erosing to find text
    N = 15
    kernel = np.zeros((N, N), dtype=np.uint8)
    kernel[(N - 1) // 2, :] = 1
    
    dilated_image = cv2.dilate(debordered, kernel, iterations=3)
    if name:
        cv2.imwrite(f"./img_temp/{name}_4_dilated_image.png", dilated_image)

    eroded_image = cv2.erode(dilated_image, kernel, iterations=3)
    if name:
        cv2.imwrite(f"./img_temp/{name}_5_eroded_image.png", eroded_image)

    N = 3
    kernel = np.zeros((N, N), dtype=np.uint8)
    kernel[:, (N - 1) // 2] = 1

    dilated_image = cv2.dilate(eroded_image, kernel, iterations=1)
    if name:
        cv2.imwrite(f"./img_temp/{name}_6_dilated_image.png", dilated_image)
    
    eroded_image = cv2.erode(dilated_image, kernel, iterations=1)
    eroded_image = eroded_image.astype(np.uint8)
    
    if name:
        cv2.imwrite(f"./img_temp/{name}_7_eroded_image.png", eroded_image)

    eroded_image = separate_img_line(eroded_image)
    if name:
        cv2.imwrite(f"./img_temp/{name}_8_eroded_image.png", eroded_image)
    
    # Find contours and their bounding boxes
    contours, _ = cv2.findContours(eroded_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    line_bounding_rects = get_rects_from_contours(contours)
    
    # # For debugging
    if name:
        blank_image = 255 * np.ones(gray.shape, dtype="uint8")
        for idx, rect in enumerate(line_bounding_rects):
            x0, y0, x1, y1 = rect
            cv2.rectangle(blank_image, (x0, y0), (x1, y1), (0, 255, 0), 2)
            idx += 1
            cv2.putText(blank_image, str(idx), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), lineType=cv2.LINE_AA)

        cv2.imwrite(f"./img_temp/{name}_9_blank_image.png", blank_image)
    return line_bounding_rects


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


def separate_img_line(img):
    """Handling closed lines"""
    MEAN_ROW_THRE = 100
    NUM_LINE_ADDED = 1
    LINE_MEAN_DIFF = 45

    line = np.zeros((1, img.shape[1]), dtype=np.uint8)
    for idx, row in enumerate(img):
        mean = np.mean(row)
        if mean < MEAN_ROW_THRE:
            if 0 < idx < len(img) - NUM_LINE_ADDED + 1:
                if (
                    np.mean(img[idx - 1]) > 0
                    and abs(np.mean(img[idx - 1]) - mean) > LINE_MEAN_DIFF
                ):
                    for i in range(NUM_LINE_ADDED):
                        img[idx + i] = line
    
    return img
