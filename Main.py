from LoadCSV import LoadCSV
from ZabbixAPI import ZabbixAPI
from getpass import getpass


class Main:
    def __init__(self, filename, user, password, url):
        self.hostlist = LoadCSV(filename).export()
        self.zabbix = ZabbixAPI(user, password, url)
        self.zabbix.login()

    def debug(self):
        print(self.hostlist)
        for line in self.hostlist:
            print(line['Templates'].split(','))
            print(line['Groups'])
            print(line['HostName'])
            print(line['AgentInterface'])

    def chk_ip(self, ip_str):
        sep = ip_str.split('.')
        if len(sep) != 4:
            return False
        for i, x in enumerate(sep):
            try:
                int_x = int(x)
                if int_x < 0 or int_x > 255:
                    return False
            except ValueError as e:
                return False
        return True

    def create_host(self):
        for line in self.hostlist:
            if self.chk_ip(line['AgentInterface']) is False:
                continue
            self.zabbix.get_template_id(line['Templates'].split(','))
            self.zabbix.get_group_id(line['Groups'])
            self.zabbix.create_host(line['HostName'], line['AgentInterface'])


if __name__ == '__main__':
    zabbix_csv = 'hostlist.csv'
    zabbix_id = input('Zabbix Account:')
    zabbix_pwd = getpass('Zabbix Password:')
    zabbix_api = 'http://192.168.1.11/zabbix/api_jsonrpc.php'

    a = Main(zabbix_csv, zabbix_id, zabbix_pwd, zabbix_api)
    a.create_host()
    #a.debug()
