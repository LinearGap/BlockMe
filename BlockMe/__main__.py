from asyncio import subprocess
from blocking import blocking
from config import config

from scheduler import scheduler
import psutil
import os
import subprocess
import time

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

        time_tuple = time_to_tuple("23:01")
        now = time.localtime(time.time())

        hours_diff = time_tuple[0] - now.tm_hour
        mins_diff = time_tuple[1] - now.tm_min

        print(f'h{hours_diff}: m{mins_diff}')

        seconds = ((hours_diff * 60) * 60) + (mins_diff * 60)    
        print(f's{seconds}')

        """
        cwd = os.getcwd()
        path = cwd + '/BlockMe/scheduler.py'
        pr = subprocess.Popen(['python', path])
        print(pr.pid)
        print(psutil.Process(pr.pid))
        time.sleep(15)
        psutil.Process(pr.pid).kill()
        print(time.localtime(time.time()))
        """
        return 0


    def is_strtime_passed(strtime):
        """
        Check if string in format "HH:MM" has already passed for today
        """

        hour = int(strtime[0:2])
        minutes = int(strtime[-2:])
        print(f'H{hour}:M{minutes}')

        now = time.localtime(time.time())

        if hour < now.tm_hour:
            # Hour is before current time therefore time has elapsed
            return True

        if hour == now.tm_hour:
            # Same hour, check if minutes is less
            if minutes <= now.tm_min:
                return True

        return False

    def time_to_tuple(strtime):
        """
        Convert from a 'HH:MM' time string to a (hour: HH, minute: MM) tuple
        """
        hour = int(strtime[0:2])
        minutes = int(strtime[-2:])
        time_tuple = (hour, minutes)

        return time_tuple

    main()