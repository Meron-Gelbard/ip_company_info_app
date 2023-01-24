import requests


class VisitorIpRequest:
    def __init__(self):
        self.API_GET_URL = 'http://ip-api.com/json/'

    def check_ip(self, ip):
        response = requests.get(url=self.API_GET_URL+ip).json()
        return response


