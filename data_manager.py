import requests

SHEETY_USERNAME = "dee_"
SHEETY_PASSWORD = "livurlyf15"
get_sheet_endpoint = "https://api.sheety.co/ebaa7c9be6c363ad7e256c7dc01161ec/myFlightDeals/prices"
get_users_sheet_endpoint = "https://api.sheety.co/ebaa7c9be6c363ad7e256c7dc01161ec/myFlightDeals/users"


class DataManager:

    def __init__(self):
        self.customer_data = None
        self.destination_data = {}

    def get_destination_data(self):
        # 2. Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(
            url=get_sheet_endpoint,
            auth=(
                SHEETY_USERNAME,
                SHEETY_PASSWORD
            )
        )
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    # 6. In the DataManager Class make a PUT request and use the row id from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{get_sheet_endpoint}/{city['id']}",
                json=new_data,
                auth=(
                    SHEETY_USERNAME,
                    SHEETY_PASSWORD
                )
            )
            print(response.text)

    def get_customer_emails(self):
        customers_endpoint = get_users_sheet_endpoint
        response = requests.get(
            url=customers_endpoint,
            auth=(
                SHEETY_USERNAME,
                SHEETY_PASSWORD
            )
        )
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
