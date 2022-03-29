from hosts import hosts as Host

if __name__ == '__main__':
    hosts = Host()
    print(hosts.read_backup())
    hosts.write_backup()