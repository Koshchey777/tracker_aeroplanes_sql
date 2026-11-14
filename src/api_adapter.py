from requests import get
from abc import ABC, abstractmethod

class BaseApi(ABC):

    @abstractmethod
    def get_response(self):
        pass

    @abstractmethod
    def get_data(self):
        pass


class NominatimApi(BaseApi):

    def __init__(self, country):
        self.__openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self.__headers_nominatim = {
                    'User-Agent': 'test-app/1.0',
                }

        self.__params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }

    def get_response(self):
        response = get(url=self.__openstreetmap_url, params=self.__params_nominatim, headers=self.__headers_nominatim)
        response.raise_for_status()
        return response.json()

    def get_data(self):
        return self.get_response()[0].get('boundingbox')


class OpenskyApi(BaseApi):

    def __init__(self, geo_coordinates):
        self.__opensky_url = 'https://opensky-network.org/api/states/all?'
        self.__params = {
                    'lamin': geo_coordinates[0],
                    'lamax': geo_coordinates[1],
                    'lomin': geo_coordinates[2],
                    'lomax': geo_coordinates[3],
                }


    def get_response(self):
        response = get(url=self.__opensky_url, params=self.__params)
        response.raise_for_status()
        return response.json()

    def get_data(self):
        airplanes = []
        data = self.get_response()['states']
        for airplane in data:
            airplanes.append({'ica': airplane[0],
                              'callsign': airplane[1].strip(),
                              'altitude': airplane[7],
                              'on_ground': airplane[8],
                              'velocity': airplane[9]})

        return airplanes

nm_api = NominatimApi('Canada')
coords = nm_api.get_data()
print(coords)

opensky_api = OpenskyApi(coords)
print(opensky_api.get_data())
