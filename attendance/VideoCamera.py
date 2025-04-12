# camera.py
import cv2
import os
import time
from flask import Response
from pathlib import Path
import uuid
from contextlib import contextmanager
from typing import Callable

# https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_alt2.xml
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor = 0.6
datasets = 'datasets'


class VideoCamera:
    def __new__(cls, *args, **kwargs):
        if getattr(cls, '_instance', False):
            return cls._instance

        cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'video'):
            self.video = cv2.VideoCapture(0)
            # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

    def get_frame(self) -> bytes:
        success, image = self.video.read()

        if not success:
            return b''

        image = cv2.resize(image, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in face_rects:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def save_to_dataset(self) -> str:
        data_set_size: int = 20
        sub_folder = 'Tapan_1'
        (width, height) = (130, 100)

        dst_dir = Path(__file__).parent / Path(f'{datasets}/{sub_folder}')
        dst_dir.mkdir(parents=True, exist_ok=True)
        num_of_files = len([_ for _ in dst_dir.glob('*.*')])

        if num_of_files >= data_set_size:
            return ""

        for _ in range(data_set_size - num_of_files):
            success, image = self.video.read()
            image = cv2.resize(image, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in face_rects:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (width, height))
                cv2.imwrite(f'{dst_dir/Path(str(uuid.uuid4()))}.png', face_resize)
        return f'{data_set_size} image captured.'
