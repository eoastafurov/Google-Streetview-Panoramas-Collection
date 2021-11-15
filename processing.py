import google_streetview.api
import numpy as np
import cv2

from geo_utils import Point
from url_utils import UrlUtils
from json_parser import JsonParser
from collected_images_utils import CollectedImage


class Processing:
    @staticmethod
    def request_image(params: {}) -> np.ndarray:
        results = google_streetview.api.results(params)
        results.download_links(dir_path='tmp/')
        image = cv2.imread('tmp/gsv_0.jpg')
        return image

    @staticmethod
    def multidirectional(point: Point) -> CollectedImage:
        forward_params = UrlUtils.get_params_for_url_request_with_snapping(point)
        lat, lng = (float(num) for num in forward_params[0]['location'].split(', '))
        backw, left, right = (
            UrlUtils.get_params_for_url_request(
                location=Point(
                    lat=lat,
                    lng=lng
                ),
                heading=float(int(forward_params[0]['heading']) + shift) % 360
            )
            for shift in [180, 90, 270]
        )

        collected = CollectedImage()
        collected.set_multidirectional(
            forw=Processing.request_image(forward_params),
            backw=Processing.request_image(backw),
            left=Processing.request_image(left),
            right=Processing.request_image(right),
            location=Point(lat, lng)
        )
        return collected

    @staticmethod
    def randomdirectional(point: Point) -> CollectedImage:
        forward_params = UrlUtils.get_params_for_url_request_with_snapping(point)
        lat, lng = (float(num) for num in forward_params[0]['location'].split(', '))

        shifts_list = [40 * i for i in range(1, 9)]
        params_list = [
            UrlUtils.get_params_for_url_request(
                location=Point(
                    lat=lat,
                    lng=lng
                ),
                heading=float(int(forward_params[0]['heading']) + shift) % 360
            )
            for shift in shifts_list
        ]
        params_list.append(forward_params)
        images_list = [
            Processing.request_image(params)
            for params in params_list
        ]
        collected = CollectedImage()
        collected.set_randomdirectional(images_list, Point(lat, lng))

        return collected

    @staticmethod
    def process_json(
            path_to_json: str,
            root_path: str,
            proc_type='multidirectional'
    ):
        assert proc_type in ['multidirectional', 'randomdirectional']

        json_parser = JsonParser(path_to_json=path_to_json)

        for zone_number, zone in enumerate(json_parser.zones):
            if zone.is_processed is False:
                for point in zone.random_choice_from_square(num=zone.num):
                    try:
                        collected = CollectedImage()
                        if proc_type == 'multidirectional':
                            collected = Processing.multidirectional(point)
                        elif proc_type == 'randomdirectional':
                            collected = Processing.randomdirectional(point)

                        collected.dump(root_path=root_path, label=zone.label)
                    except KeyError:
                        print('Key error')
                json_parser.mark_zone_as_processed(zone_number)


Processing.process_json(
    path_to_json='zones/coords_zones.json',
    root_path='collected_images/',
    proc_type='randomdirectional'
)
