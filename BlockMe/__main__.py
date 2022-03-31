from blocking import blocking
from config import config

if __name__ == '__main__':
    def main():
        blocker = blocking()
        blocker.add_site('www.google.co.uk')
        blocker.add_site('www.nexus.net')
        blocker.add_site('http://block.me')
        blocker.add_site('https://www.net.web')
        blocker.set_redirect_address('1.1.1.1')
        blocker.activate()
        print(blocker.query_installed())
        blocker.disactivate()
        c = config()
        c.load()
        c.permanent_urls = []
        c.scheduled_urls = []
        c.save()

        return 0
    main()