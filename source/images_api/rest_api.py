import requests


class ImageAPI:
    _base_url = "http://interview.agileengine.com"
    _tkn: str
    _api_key: str

    def __init__(self, api_key):
        self._api_key = api_key
        self._get_tkn()

    def _get_tkn(self):
        response = requests.post(self._base_url + "/auth", json={"apiKey": self._api_key})
        response_json = response.json()
        if response.status_code == 401 or "auth" not in response_json:
            raise Exception("Failed to obtain token")
        self._tkn = response_json["token"]

    def get_image_ids(self):
        image_ids = []

        there_are_still_images = True
        current_page = 1
        host = self._base_url + "/images"

        while there_are_still_images:
            response = self._perform_api_request(
                host,
                params={"page": current_page}
            )
            image_ids += [image["id"] for image in response["pictures"]]
            there_are_still_images = response["hasMore"]
            current_page += 1
        return image_ids

    def get_images_with_metadata(self):
        photo_ids = self.get_image_ids()
        photos = []
        for photo_id in photo_ids:
            photos.append(self._perform_api_request(self._base_url + f"/images/{photo_id}"))
        return photos

    def _perform_api_request(self, host, params=None, json=None):
        response = requests.get(
            host,
            params=params,
            json=json,
            headers={
                "Authorization": "Bearer " + self._tkn
            })
        if response.status_code == 401:
            self._get_tkn()
            return self._perform_api_request(host, params, json)
        return response.json()
