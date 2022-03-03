from flight_data import FlightData
from pprint import pprint
import requests

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_APP_KEY = "nhD2TgmFUHQ02vWvUEoyBoJqK3JnbbLP"


class FlightSearch:

    def __init__(self):
        self.city_codes = []

    def get_destination_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {
            "apikey": "nhD2TgmFUHQ02vWvUEoyBoJqK3JnbbLP",
        }
        for city in city_name:
            query = {
                "term": city,
                "location_types": "city",
            }
            search_response = requests.get(url=location_endpoint,
                                           params=query,
                                           headers=headers)
            locations = search_response.json()["locations"]
            iata_code = locations[0]["code"]
            self.city_codes.append(iata_code)

        return iata_code

    def search_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        search_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        headers = {
            "apikey": "nhD2TgmFUHQ02vWvUEoyBoJqK3JnbbLP",
        }
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 30,
            "flight_type": "round",
            "one_for_city": 1,
            "curr": "GBP",
            "max_stopovers": 0,
        }

        response = requests.get(
            url=search_endpoint,
            params=query,
            headers=headers
        )
        try:
            data = response.json()["data"][0]
            print(f"{destination_city_code}: £{data['price']}")
        except IndexError:
            query["max_stopovers"] = 1
            response = requests.get(
                url=f"{TEQUILA_ENDPOINT}/v2/search",
                headers=headers,
                params=query,
            )
            data = response.json()["data"][0]
            pprint(data)
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][1]["cityTo"],
                destination_airport=data["route"][1]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][2]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )

            return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            return flight_data

