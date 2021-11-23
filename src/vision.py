import cv2 as cv
import numpy as np

class DebugMode:
    NONE = 0
    RECTANGLE = 1
    POINTS = 2


class Vision:
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

    line_color = (0, 255, 0)
    line_type = cv.LINE_4
    marker_color = (0, 255, 0)
    marker_type = cv.MARKER_CROSS

    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        self.needle_img = cv.cvtColor(cv.imread(needle_img_path, cv.IMREAD_UNCHANGED), cv.COLOR_RGB2GRAY)
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]
        self.method = method

    def find(self, haystack_img, threshold=0.5, debug_mode=DebugMode.NONE):
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        points = []
        if len(rectangles):
            for (x, y, w, h) in rectangles:
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                points.append((center_x, center_y))
                if debug_mode == DebugMode.RECTANGLE:
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    cv.rectangle(haystack_img, top_left, bottom_right, color=self.line_color,
                                lineType=self.line_type, thickness=2)
                elif debug_mode == DebugMode.POINTS:
                    cv.drawMarker(haystack_img, (center_x, center_y),
                                color=self.marker_color, markerType=self.marker_type,
                                markerSize=40, thickness=2)
        if debug_mode:
            cv.imshow('Matches', haystack_img)
        return points
