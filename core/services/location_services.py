import requests


class LocationServices:
    def get_destination(self, destination):
        url = "https://nominatim.openstreetmap.org/search"

        params = {
            "q": destination,
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "personal-planner-app"
        }


        response = requests.get(url=url, params=params, headers=headers)


        if response.status_code != 200:
            return None

        data = response.json()

        if not data:
            return None

        location = data[0]

        return {
            "name": location.get("display_name"),
            "lat": location.get("lat"),
            "lon": location.get("lon")
        }