import numpy as np
import cv2
import os
import random

from geo_utils import Point
from image_utils import ImageUtils
from typing import List


class CollectedImage:
    """
    fields:
        1. Multidirectional: dict with keys:
            'forward_view',
            'backward_view',
            'left_view',
            'right_view'.

        2. Randomdirectional: list with images
    """
    def __init__(self):
        self.multidirectional = None
        self.randomdirectional = None
        self.location = None

    def set_randomdirectional(self, imgs: List[np.ndarray], location: Point):
        self.randomdirectional = imgs.copy()
        self.location = location

    def set_multidirectional(
            self,
            forw: np.ndarray,
            backw: np.ndarray,
            left: np.ndarray,
            right: np.ndarray,
            location: Point
    ):
        self.multidirectional = {
            'forward_view': forw,
            'backward_view': backw,
            'left_view': left,
            'right_view': right
        }
        self.location = location

    def dump(self, root_path: str, label: str):
        def gen_name_from_loc(idx: int):
            return root_path \
                   + label + '/' \
                   + 'gsv_' \
                   + '{}_{}'.format(round(self.location.lat, 7), round(self.location.lng, 7)) \
                   + '_{}'.format(idx) \
                   + '.jpg'

        images_to_save = list()

        if self.multidirectional is not None:
            images_to_save = list(dict(self.multidirectional).values())

        if self.randomdirectional is not None:
            images_to_save = list(self.randomdirectional)

        for i, image in enumerate(images_to_save):
            name = gen_name_from_loc(i)
            while os.path.exists(name):
                name = gen_name_from_loc(int(random.random() * 10 ** 3))
            cv2.imwrite(name, ImageUtils.remove_google_label_from_image(image))
