from blocking import blocking

if __name__ == '__main__':
    def main():
        blocker = blocking()
        blocker.add_site('www.google.co.uk')
        blocker.add_site('www.nexus.net')
        blocker.add_site('http://block.me')
        blocker.add_site('https://www.net.web')
        blocker.activate()
        print(blocker.query_installed())
        blocker.disactivate()
        return 0
    main()