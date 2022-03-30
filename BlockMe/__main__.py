from hosts import hosts as Host

if __name__ == '__main__':
    def main():
        hosts = Host()
        print(hosts.get())
        hosts.add('www.facebook.co.uk')
        hosts.add_list(['google.com', 'next.com', 'youtube.com', 'more.com'])
        print(hosts.get())
        hosts.save()
        return 0
    main()