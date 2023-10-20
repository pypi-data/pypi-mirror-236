import logging    def add_widget_to_screen(self):
        """Not implemented"""
        raise NotImplementedError(self.not_implemented_text)


import requests
import urllib3

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# noinspection RequestsNoVerify
class FeatureToggleUi:
    def __init__(self, url, username, password):
        self.url = str(url)
        self.username = str(username)
        self.password = str(password)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept': '*/*',
            'Connection': 'close',
        }
        self.not_implemented_text = "This Function is not yet implemented"

    def create_feature(self, ft, data):
        """
        Creating Feature
        :param ft:  Name of Feature
        :param data: Json Data for creating Feature
        :return: Status Code
        """
        logging.info(f"Creating {ft} at {self.url}")
        response = requests.post(
            self.url,
            headers=self.headers,
            json=data,
            verify=False,
            auth=(self.username, self.password),
        )
        if response.status_code == 201 and response.text == '':
            logging.info(f"{ft} added")
        elif response.status_code == 500 and 'E11000 duplicate key error collection' in response.text:
            logging.error(f"{ft} already presented")
        elif response.status_code == 500 and 'null.pointer.error' in response.text:
            logging.error(f"Data was not correct")
        else:
            logging.error({response.status_code, response.text})
            input("Press Enter to continue...\n")
        return response.status_code

    def create_user_list(self, ft):
        """
        Creating empty user list in Feature
        :param ft: Name of Feature
        :return: Status Code
        """
        logging.info(f"Creating user list in {ft} at {self.url}")
        response = requests.post(
            f'{self.url}/{ft}/users',
            headers=self.headers,
            json=[],
            verify=False,
            auth=(self.username, self.password),
        )
        if response.status_code == 200:
            logging.info(f"User list successful added to {ft}")
        else:
            logging.error({response.status_code, response.text})
            input("Press Enter to continue...\n")
        return response.status_code

    def add_user_to_feature(self, ft, data):
        """
        Adding users to Feature
        :param ft: Name of Feature
        :param data: List of users
        :return: Status Code
        """
        logging.info(f"Adding users to {ft} at {self.url}")
        response = requests.put(
            f'{self.url}/{ft}/users',
            headers=self.headers,
            json=data,
            verify=False,
            auth=(self.username, self.password),
        )
        if response.status_code == 200 and response.text == '':
            logging.info(f"User successful added to {ft}")
        elif response.status_code == 400 and 'CUS_INVALID_ERROR' in response.text:
            logging.error(f"Incorrect user list")
        elif response.status_code == 500 and 'null.pointer.error' in response.text:
            logging.error(f"Incorrect data")
            logging.error(f"{response.status_code, response.text}")
        else:
            logging.error({response.status_code, response.text})
        return response.status_code
