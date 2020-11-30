import requests


class ImageAPI:
    _host = "http://interview.agileengine.com"
    _token: str
    _api_key: str

    def __init__(self, api_key):
        self._api_key = api_key
        self._obtain_token()

    def _obtain_token(self):
        """Method to obtain auth token from AgileEngine public API
        raises:
            Exception: When can't obtain token
        """
        url = self._host + "/auth"
        response = requests.post(url, json={"apiKey": self._api_key})
        response_json = response.json()
        if response.status_code == 401 or "auth" not in response_json:
            raise Exception("Failed to obtain token")
        self._token = response_json["token"]

    def get_image_ids(self):
        """Get list of image's ids from API

        Returns:
                photo_ids ([str]): The list of photo ids
        """
        image_ids = []

        there_are_still_images = True
        current_page = 1
        url = self._host + "/images"

        while there_are_still_images:
            response = self._perform_api_request(
                "get",
                url,
                params={"page": current_page}
            )
            image_ids += [image["id"] for image in response["pictures"]]
            there_are_still_images = response["hasMore"]
            current_page += 1
        return image_ids

    def get_image_metadata(self, image_id):
        """Returns the photo metada

        Parameters:
                image_id (str): The image id

        Returns:
                image_data (dict): Dict with information about the image
        """
        url = self._host + f"/images/{image_id}"
        return self._perform_api_request("get", url)

    def get_images_with_metadata(self):
        """Returns the photos with metadata

        Returns:
                image ([dict]): List of dicts with information about each image
        """
        image_ids = self.get_image_ids()
        images = []
        for image_id in image_ids:
            images.append(self.get_image_metadata(image_id))
        return images

    def _perform_api_request(self, method, url, params=None, json=None):
        """Makes a HTTP request to the API with specified parameters

        Parameters:
                method (str): A request method
                url (str): An url
                params (dict): GET parameters
                json (dict): POST json parameters

        Returns:
                data (dict): Response from API

        raises:
            Exception: When can't obtain token (from __obtain_token)
        """
        headers = {
            "Authorization": "Bearer " + self._token
        }
        response = getattr(requests, method)(url, params=params, json=json, headers=headers)
        if response.status_code == 401:
            self._obtain_token()
            return self._perform_api_request(method, url, params, json)
        return response.json()
