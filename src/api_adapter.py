from abc import ABC, abstractmethod

from requests import get


class BaseApi(ABC):

    @abstractmethod
    def get_response(self):
        pass

    @abstractmethod
    def get_data(self):
        pass


class NominatimApi(BaseApi):

    def __init__(self, country):
        self.__openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.__headers_nominatim = {
            "User-Agent": "test-app/1.0",
        }

        self.__params_nominatim = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

    def get_response(self):
        """Получение ответа на запрос от Nominatim"""
        response = get(
            url=self.__openstreetmap_url,
            params=self.__params_nominatim,
            headers=self.__headers_nominatim,
        )
        response.raise_for_status()
        return response.json()

    def get_data(self):
        """Получение координат страны"""
        return self.get_response()[0].get("boundingbox")


class OpenskyApi(BaseApi):

    def __init__(self, geo_coordinates):
        self.__opensky_url = "https://opensky-network.org/api/states/all?"
        self.__params = {
            "lamin": geo_coordinates[0],
            "lamax": geo_coordinates[1],
            "lomin": geo_coordinates[2],
            "lomax": geo_coordinates[3],
        }

    def get_response(self):
        """Получение ответа на запрос от Opensky"""
        response = get(url=self.__opensky_url, params=self.__params)
        response.raise_for_status()
        return response.json()

    def get_data(self):
        """Получение информации о самолетах"""
        airplanes = []
        data = self.get_response()["states"]
        response_data = self.get_response()
        states = response_data.get('states')
        if not states:
            return airplanes
        for airplane in states:
            airplanes.append(
                {
                    "ica": airplane[0],
                    "callsign": airplane[1].strip() if airplane[1] else "",
                    "altitude": airplane[7],
                    "on_ground": airplane[8],
                    "velocity": airplane[9],
                }
            )

        return airplanes
