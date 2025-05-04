import math
import cv2
import numpy as np


def get_rect(countur_item):
    x1 = countur_item[0][0][0]
    y1 = countur_item[0][0][1]
    x2 = countur_item[2][0][0]
    y2 = countur_item[2][0][1]
    return (x1,y1), (x2,y2)


def dist(point1, point2) -> float:
    d1 = point1[0] - point2[0]
    d2 = point1[1] - point2[1]
    return math.sqrt(d1*d1 + d2*d2)


def filter_approx_countours(approx) -> bool:
    if len(approx) != 4:
        return False 

    x0, y0 = approx[0][0]
    x2, y2 = approx[2][0]

    if abs(x2 - x0) < 20 or abs(y2 - y0) < 10:
        return False

    horizontal1 = dist(approx[0][0], approx[1][0])
    horizontal2 = dist(approx[2][0], approx[3][0])
    vertical1 = dist(approx[0][0], approx[3][0])
    vertical2 = dist(approx[1][0], approx[2][0])

    if horizontal2 == 0 or vertical2 == 0:
        return False

    ratio_h = horizontal1 / horizontal2
    ratio_v = vertical1 / vertical2

    if abs(ratio_h - 1) > 0.6: 
        return False
    if abs(ratio_v - 1) > 0.6:
        return False

    return True


def merge_nearby_rects(rects, margin=20):
    def expand_rect(rect, margin):
        x, y, w, h = rect
        return (x - margin, y - margin, w + 2 * margin, h + 2 * margin)

    def rects_overlap(r1, r2):
        x1, y1, w1, h1 = r1
        x2, y2, w2, h2 = r2
        return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

    used = [False] * len(rects)
    merged = []

    for i in range(len(rects)):
        if used[i]:
            continue

        base = rects[i]
        group = [base]
        used[i] = True

        changed = True
        while changed:
            changed = False
            for j in range(len(rects)):
                if used[j]:
                    continue
                for r in group:
                    if rects_overlap(expand_rect(r, margin), expand_rect(rects[j], margin)):
                        group.append(rects[j])
                        used[j] = True
                        changed = True
                        break

        x_coords = [x for (x, _, w, _) in group] + [x + w for (x, _, w, _) in group]
        y_coords = [y for (_, y, _, h) in group] + [y + h for (_, y, _, h) in group]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        merged.append((x_min, y_min, x_max - x_min, y_max - y_min))

    return merged