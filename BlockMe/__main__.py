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
        
        cwd = os.getcwd()
        path = cwd + '/BlockMe/background_process.py'
        pr = subprocess.Popen(['python', path])
        print(pr.pid)
        print(psutil.Process(pr.pid))
        
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