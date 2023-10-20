import json
import logging

import requests
import urllib3

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# noinspection RequestsNoVerify
class WidgetManagementUi:
    def __init__(self, url, username, password):
        self.url = str(url)
        self.username = str(username)
        self.password = str(password)
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Connection': 'close',
        }

    def search_widget(self, widget: str):
        """
        Search widget
        :param widget: Name of widget
        :return: Widget ID
        """
        logging.info(f"Searching {widget} at {self.url}")
        params = {
            'page': '0',
            'searchQuery': widget,
            'size': '1',
        }
        try:
            response = requests.get(
                self.url,
                params=params,
                headers=self.headers,
                verify=False,
                auth=(self.username, self.password),
            )
            widget_id = json.loads(response.content)['widgets'][0]['id']
            return widget_id
        except IndexError:
            logging.warning('Not found Widget ID')

    def create_widget(self, widget: str, data: json, update: bool):
        """
        Creating widget
        :param widget: Name of widget
        :param data: Widget JSON
        :param update: Boolean
        :return: Status Code
        """
        logging.info(f"Creating {widget} at {self.url}")
        response = requests.post(
            self.url,
            headers=self.headers,
            json=data,
            verify=False,
            auth=(self.username, self.password),
        )
        if response.status_code == 200:
            logging.info(f"Widget {widget} successfully added")
        elif response.status_code == 400:
            logging.warning(f"Widget {widget} already presented")
            if update is True:
                self.update_widget(widget, data)
        else:
            logging.error({response.status_code, response.text})
        return response.status_code

    def delete_widget(self, widget: str, lotus: str):
        """
        Deleting widget
        :param widget: Name of widget
        :param lotus: Number of lotus request
        :return: Status Code
        """
        widget_id = self.search_widget(widget)
        logging.info(f"Deleting {widget} at {self.url}")
        params = {
            'reason': f'{lotus}',
            'deleteFromAllScreens': True,
        }
        response = requests.delete(
            f'{self.url}/{widget_id}',
            params=params,
            headers=self.headers,
            verify=False,
            auth=(self.username, self.password),
        )
        if response.status_code == 200:
            logging.info(f"{widget} removed")
        elif response.status_code == 400:
            logging.error(f"{widget} does not exist")
        else:
            logging.error({response.status_code, response.text})
        return response.status_code

    def update_widget(self, widget: str, data: json):
        """
        Updating widget JSON
        :param widget: Name of widget
        :param data: Widget JSON
        :return: Status Code
        """
        widget_id = self.search_widget(widget)
        logging.info(f"Updating {widget} at {self.url}")
        response = requests.put(
            f'{self.url}/{widget_id}',
            headers=self.headers,
            json=data,
            verify=False,
            auth=(self.username, self.password),
        )
        if response.status_code == 200:
            logging.info(f"Widget {widget} successfully updated")
        else:
            logging.error({response.status_code, response.text})
        return response.status_code
