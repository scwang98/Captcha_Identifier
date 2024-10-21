
import numpy as np
import torch
import base64

import sys
import os
# 丑陋至极
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'yolov5')))

from yolov5.models.common import DetectMultiBackend
from yolov5.utils.augmentations import letterbox
from yolov5.utils.general import (
    cv2,
    non_max_suppression,
    scale_boxes,
)


class WordDetector(object):

    def __init__(self, **kwargs):
        
        device = torch.device('cpu')
        self.model = DetectMultiBackend("models/word_detect.pt", device=device, dnn=False, data="captcha.yaml", fp16=False)
        imgsz = (640, 640)  # check image size
        self.model.warmup(imgsz=(1, 3, *imgsz))  # warmup


    def detect(self, image: bytes):

        im0 = np.frombuffer(image, np.uint8)
        im0 = cv2.imdecode(im0, cv2.IMREAD_COLOR)

        stride, pt = self.model.stride, self.model.pt
        imgsz = (640, 640)  # check image size


        im = letterbox(im0, imgsz, stride=stride, auto=pt)[0]  # padded resize
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)  # contiguous

        im = torch.from_numpy(im).to(self.model.device)
        im = im.half() if self.model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim

        pred = self.model(im, augment=False, visualize=False)
        pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45, max_det=1000)

        results = []
        for det in pred:
            if len(det) <= 0:
                continue
            det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
            for *xyxy, conf, cls in reversed(det):
                results.append([t.item() for t in xyxy])

        return results

