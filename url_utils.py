from geo_utils import GeoUtils, Point
from google_developer_key import get_developer_key


class UrlUtils:
    @staticmethod
    def get_params_for_url_request_with_snapping(point: Point) -> {}:
        snapped = GeoUtils.snap_point_to_closest_road(point, radius=300)
        direction = GeoUtils.road_direction(snapped, print_distance=True)

        return UrlUtils.get_params_for_url_request(location=snapped, heading=direction)

    @staticmethod
    def get_params_for_url_request(
            location: Point,
            heading: float,
            radius: int = 50,
            height: int = 410,
            width: int = 640
    ):
        params = [{
            'size': '{}x{}'.format(width, height),
            'location': '{}, {}'.format(location.lat, location.lng),
            'key': '{}'.format(get_developer_key()),
            'return_error_code': True,
            'radius': radius,
            'source': 'outdoor',
            'heading': heading
        }]
        return params
