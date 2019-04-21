import csv


class LoadCSV:
    def __init__(self, filename):
        self.hostlist = []
        with open(filename, newline='', encoding='UTF-8-sig') as f:
            f_csv = csv.DictReader(f)
            for row in f_csv:
                self.hostlist.append(row)

    def export(self):
        return self.hostlist


if __name__ == '__main__':
    a = LoadCSV('hostlist.csv')
    for line in a.export():
        print(line['HostName'])
        print(line['AgentInterface'])
