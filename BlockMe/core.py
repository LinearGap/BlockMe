import argparse
from signal import SIGTERM
import subprocess
from blocking import blocking as Blocker
from config import config as Config
import os
import sys

class core():
    """
    The core class for the BlockMe application that is run from the command line
    """

    def __init__(self):
        self.__parser = argparse.ArgumentParser(prog='BlockMe', 
        description="Application to Block URLs by redirection. Uses the host file in teh background.")
        self.config = Config()
        self.config.load()

    def run(self):
        """
        Run the Block me application. Called as the main entry point
        """
        self.__parser.add_argument('command', action='store', type=str, choices=['start', 'stop', 'add', 'schedule'])
        self.__parser.add_argument('data', action='store', nargs='*')

        parsed = self.__parser.parse_args()
        self.command = parsed.command
        self.data = parsed.data

        if self.command == 'start' or self.command == 'Start':
            self.__start()
        elif self.command == 'stop' or self.command == 'Stop':
            self.__stop()

    def __start(self):
        """
        Start the BlockMe application.
        First add any permanent blocks.
        Then start the background process
        """
        blocker = Blocker()
        blocker.set_redirect_address(self.config.redirect_addr)
        for url in self.config.permanent_urls:
            blocker.add_site(url)

        blocker.activate()

        self.config.last_state = 'Starting'
        self.config.save()

        self.__start_bg()

        print("BlockMe has started!")

    def __get_script_path():
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    def __start_bg(self):
        """
        Start the background process
        """
        path = core.__get_script_path()
        bg_path = path + '/BlockMe/background_process.py'

        pr = subprocess.Popen(['python', bg_path])

    def __stop(self):
        """
        Stop any running background process and then
        restore the hosts file to default
        """
        bg_pid = self.config.scheduler_pid
        os.kill(bg_pid, SIGTERM)

        blocker = Blocker()
        blocker.restore_default()