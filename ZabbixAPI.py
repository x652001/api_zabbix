import requests
import json


class ZabbixAPI:
    def __init__(self, user, password, zabbix_url):
        # Zabbix URL
        self.zabbix_url = zabbix_url
        self.header = {"Content-Type": "application/json"}
        # login information
        self.user = user
        self.password = password
        self.auth = ""

        self.templates_id = []
        self.groups_id = []

    def login(self):
        # Parameter for zabbix API
        parameter = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.user,
                "password": self.password
            },
            "id": 1,
            "auth": None
        })
        # Get response text from zabbix API by using POST
        response = requests.post(self.zabbix_url, parameter, headers=self.header).text
        # Get key from response text
        try:
            self.auth = json.loads(response)['result']
        except KeyError:
            print("Login failed")
        print("Login Success")
        print(self.auth)

    def get_template_id(self, templates):
        # Init variable for templates_id in list
        self.templates_id = []
        # Parameter for Get TemplateID in Zabbix API
        parameter = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend",
                "filter": {
                    "host": templates
                }
            },
            "auth": self.auth,
            "id": 1
        })
        # Get response text from zabbix API by using POST
        response = requests.post(self.zabbix_url, parameter, headers=self.header).text
        # Append list templates_id from response text
        for i in json.loads(response)['result']:
            self.templates_id.append(str(i['templateid']))
        print(self.templates_id)

    def get_group_id(self, groups):
        # Init variable for groups_id in list
        self.groups_id = []
        # Parameter for Get GroupID in Zabbix API
        parameter = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": groups
                }
            },
            "auth": self.auth,
            "id": 1
        })
        # Get response text from zabbix API by using POST
        response = requests.post(self.zabbix_url, parameter, headers=self.header).text
        # Append list templates_id from response text
        for i in json.loads(response)['result']:
            self.groups_id.append(str(i['groupid']))
        print(self.groups_id)

    def create_host(self, hostname, interface_ip):
        # Put the group ID and template ID into dict
        group = []
        template = []
        for ids in self.groups_id:
            group.append({"groupid": str(ids)})
        for ids in self.templates_id:
            template.append({"templateid": str(ids)})
        # Parameter for CreateHost in Zabbix API
        parameter = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": interface_ip,
                "name": hostname,
                "interfaces": [{
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": interface_ip,
                    "dns": "",
                    "port": "10050"
                }],
                "groups": group,
                "templates": template
            },
            "auth": self.auth,
            "id": 1
        })
        # Create host with zabbix API by using POST
        response = requests.post(self.zabbix_url, parameter, headers=self.header).text
        print(response)


if __name__ == '__main__':
    zabbix = ZabbixAPI('Admin', 'zabbix', 'http://192.168.1.11/zabbix/api_jsonrpc.php')
    zabbix.login()
    zabbix.get_template_id(['check_icmp'])
    zabbix.get_group_id(['TestGroup'])
    zabbix.create_host('hello', '8.8.8.8')
