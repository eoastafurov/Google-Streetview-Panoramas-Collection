from geopy import distance
import math
import numpy as np
from termcolor import colored

from google_developer_key import get_developer_key
import google_streetview

EARTH_RAD = 6_378_000  # meters


class Point:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def __str__(self):
        return '{}, {}'.format(self.lat, self.lng)


class GeoUtils:
    @staticmethod
    def snap_point_to_closest_road(point: Point, radius=50) -> Point:
        params = [{
            'size': '10x10',
            'location': '{}, {}'.format(point.lat, point.lng),
            'key': '{}'.format(get_developer_key()),
            'return_error_code': True,
            'radius': radius,
            'source': 'outdoor'
        }]
        results = google_streetview.api.results(params)
        location = results.metadata[0]['location']
        return Point(lat=location['lat'], lng=location['lng'])

    @staticmethod
    def calculate_compass_bearing(point_a: Point, point_b: Point) -> float:
        lat1 = math.radians(point_a.lat)
        lat2 = math.radians(point_b.lat)
        diffLong = math.radians(point_b.lng - point_a.lng)

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) \
            - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360

        return compass_bearing

    @staticmethod
    def road_direction(
            coords: Point,
            print_distance: True
    ) -> []:
        """
        Get direction of the road which contains point `coords`

        1. Shift point with arg:`coords` by random values
        2. Snap shifted points to closest road (meant that
            snapped point will be on the same road as `coords`)
        3. Calculate compass bearing between this two points to
            get direction of the road.

        :param print_distance: if you need to print dist between
            original and shifted point.
        :param coords: Point that already(!) snapped to the road
        :return: compass bearing of the road (direction of
            the road).
        """

        def random_noise(eps=5):
            """
            Eps:
                if 1: distance ~~ 0 m
                if 2: distance ~~ 0-5 m
                if 3: distance ~~ 5-10 m
                if 4: distance ~~ 10-15 m
                if 5: distance ~~ 15-25 m
                if 6: distance ~~ 20-30 m
            """
            noise = np.random.uniform(eps * 3 * 10 ** (-5), eps * 4 * 10 ** (-5))
            sign = -1 * round(np.random.uniform(0, 1))
            return noise * sign if sign != 0 else noise

        # Generating shifted coords with noise
        noised = Point(
            lat=coords.lat + random_noise(),
            lng=coords.lng + random_noise()
        )
        # print('Snapped point: {}'.format(coords))

        # Snapping to the road
        noised = GeoUtils.snap_point_to_closest_road(noised)
        # print('Noised point: {}'.format(noised))
        dist = distance.distance((coords.lat, coords.lng), (noised.lat, noised.lng)).km * 1000

        if dist > 0 and print_distance:
            print(colored('Distance: {} meters'.format(dist), 'green'))
        else:
            print(colored('Distance: {} meters'.format(dist), 'red'))

        compass_bearing = GeoUtils.calculate_compass_bearing(coords, noised)

        return compass_bearing
