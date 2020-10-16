import requests
from math import radians, cos, sin, asin, sqrt
import json


def distance(lat1, lat2, lon1, lon2, km=False):
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in
    r = 6371
    r = r * 1000 if not km else r

    # calculate the result
    return (c * r)


def get_coordinates_info(lon, lat):
    """
    Request from geocode.arcgis API an info about (lat, lon) coordinates

    :param lon: a number for Longitude
    :param lat: a number for Latitude
    :return: dict if found data else None
    """

    path = r"https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode?" \
              "location={}%2C{}&langCode=en&outSR=&forStorage=false&f=pjson".format(lon, lat)

    x = requests.get(path)
    if x.ok:
       return json.loads(x.text)


def combinations_points(iterable, r):
    '''

    :param iterable:  dataframe of the csv file
    :param r: 2 for the combination length
    :return: list of dict  = [{'name': 'AB', 'distance': 22},
                              {'name': 'AC', 'distance': 77,
                              {'name': 'BC', 'distance': 321,]
    '''
    pool = tuple(tuple(x) for x in iterable.to_records())
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    try:
        yield {'name': f"{pool[indices[0]][0]}{pool[indices[1]][0]}",
               'distance': distance(lat1=pool[indices[0]][1],
                                    lat2=pool[indices[1]][1],
                                    lon1=pool[indices[0]][2],
                                    lon2=pool[indices[1]][2])}

    except IndexError:
        pass

    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1

        try:
            yield {'name': f"{pool[indices[0]][0]}{pool[indices[1]][0]}",
                   'distance': distance(lat1=pool[indices[0]][1],
                                        lat2=pool[indices[1]][1],
                                        lon1=pool[indices[0]][2],
                                        lon2=pool[indices[1]][2])}
        except IndexError:
            pass
