import numpy as np
import json
from pathlib import Path

IMG_EXTENSIONS = ('png', 'jpg', 'jpeg', 'bmp')


def extract_boxes_from_result(result, class_names, score_thr=0.3):
    bboxes_res, segm_result = result
    bboxes = np.vstack(bboxes_res)
    labels = [
        np.full(bbox.shape[0], i, dtype=np.int32)
        for i, bbox in enumerate(bboxes_res)
    ]
    labels = np.concatenate(labels)

    assert bboxes.ndim == 2
    assert labels.ndim == 1
    assert bboxes.shape[0] == labels.shape[0]
    assert bboxes.shape[1] == 4 or bboxes.shape[1] == 5
    assert bboxes.shape[1] == 5
    scores = bboxes[:, -1]
    inds = scores > score_thr
    bboxes = bboxes[inds, :]
    labels = labels[inds]

    instances = []
    for bbox, label in zip(bboxes, labels):
        bbox_int = [int(i) for i in bbox.astype(np.int32)[:4]]
        label_text = class_names[label] if class_names is not None else f'cls {label}'
        instances.append({'bbox': bbox_int, 'label': label_text, 'score': float(bbox[-1])})
    return instances


def has_image_extension(path: Path, allowed_extensions=IMG_EXTENSIONS):
    return any(path.name.lower().endswith(e.lower()) for e in allowed_extensions)


def load_predictions(path):
    with open(path, 'r') as f:
        return json.load(f)


def crop_img_to_bbox(img, bbox):
    x1, y1, x2, y2 = bbox
    return img[y1:y2, x1:x2]

def convert_to_xywh(bbox):
    x1, y1, x2, y2 = bbox
    return x1, y1, x2 - x1, y2 - y1
