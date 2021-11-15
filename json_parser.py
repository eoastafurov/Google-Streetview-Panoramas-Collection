import numpy as np
from geo_utils import Point
import json


class JsonParser:
    class ParseUtils:
        @staticmethod
        def random_choice_from_square(point_bl: Point, point_ur: Point, num=3) -> []:
            x_axis = np.random.uniform(low=point_bl.lat, high=point_ur.lat, size=num)
            y_axis = np.random.uniform(low=point_bl.lng, high=point_ur.lng, size=num)

            points = [Point(x_axis[i], y_axis[i]) for i in range(num)]
            return points

    class Zone:
        def __init__(self, params: {}):
            self.bottom_left = params['bottom_left']
            self.upper_right = params['upper_right']
            self.is_processed = params['is_processed']
            self.label = params['label']
            self.description = params['description']
            self.num = int(params['num'])

            self.point_bl = Point(
                lat=self.bottom_left[0],
                lng=self.bottom_left[1]
            )
            self.point_ur = Point(
                lat=self.upper_right[0],
                lng=self.upper_right[1]
            )

        def random_choice_from_square(self, num=3) -> []:
            x_axis = np.random.uniform(low=self.point_bl.lat, high=self.point_ur.lat, size=num)
            y_axis = np.random.uniform(low=self.point_bl.lng, high=self.point_ur.lng, size=num)

            points = [Point(x_axis[i], y_axis[i]) for i in range(num)]
            return points

    def __init__(self, path_to_json: str):
        with open(path_to_json, 'r') as f:
            self.zones_params = json.load(f)['zones']
        self.path_to_json = path_to_json

        self.zones = []
        for zone_params in self.zones_params:
            self.zones.append(self.Zone(zone_params))

    def mark_zone_as_processed(self, idx: int):
        self.zones_params[idx]['is_processed'] = True
        self.dump()

    def dump(self):
        with open(self.path_to_json, 'w') as file:
            json.dump({'zones': self.zones_params}, file, indent=4)
