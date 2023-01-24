import json
from visitor_ip import VisitorIpRequest
from flask import request


class VisitorManager:
    def __init__(self):
        with open('visitors.json', 'r') as data:  # load visitors.json data
            self.visitor_list = json.load(data)
        self.new_visitor = None
        self.ip_checker = VisitorIpRequest()

    def get_ip(self):  # Returns client IP address
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:  # get user ip
            visitor_ip = request.environ['REMOTE_ADDR']
        else:
            visitor_ip = request.environ['HTTP_X_FORWARDED_FOR']

        return visitor_ip

    def ip_visited(self, visitor_ip):  # Returns bolean value if clients IP has visited before.
        if visitor_ip not in (vst['visitor_ip'] for vst in self.visitor_list['visitors']):
            return False
        else:
            return True

    def list_new_visitor(self, visitor_ip):  # Lists a new visitor IP into visitors.json
        response = self.ip_checker.check_ip(visitor_ip)
        name = request.form.get("name")
        try:
            ip_owner = response['as']
        except KeyError:
            ip_owner = 'Not found.'

        self.new_visitor = {"id": len(self.visitor_list['visitors']) + 1,
                            "visitor_ip": visitor_ip,
                            "name": name,
                            "ip_owner": ip_owner}
        self.visitor_list['visitors'].append(self.new_visitor)

        with open('visitors.json', 'w') as file:
            json.dump(self.visitor_list, file, indent=2)

