import os
from config import config as Config
from blocking import blocking as Blocker
from scheduler_process import scheduler_process as Scheduler
import signal

class background_process():
    """
    Class that is the background process runner. This is what runs in
    the background to ensure scheduled blocks run as they should.
    This will be opened by Popen in a separate script as needs to run in
    the systems background.
    """

    def __init__(self):
        # Get the process id for this running process
        self.__pid = os.getpid()

        # Get the config and create a blocker
        self.config = Config()
        self.blocker = Blocker()

        # Create the scheduler
        self.scheduler = Scheduler(self.config, self.blocker)

        # Load the config vars. Then immediately update the process id 
        # and save
        self.config.load()
        self.config.scheduler_pid = self.__pid
        self.config.save()

        # Setup signals
        signal.signal(signal.SIGTERM, self.exit)
        
        # Start the process and any inner loops
        self.start_process()

        # End the process
        self.stop_process()

    def start_process(self):
        # Update the config as this is now running
        self.config.last_state = 'Running'
        self.config.save()

        self.scheduler.start()

    def stop_process(self):

        # Update the config as this is not running
        self.config.last_state = 'Shutdown'
        self.config.save()

        # Restore to the default hosts
        self.blocker.restore_default()

    def exit(self, *args):
        """
        Called when process is terminated
        """
        self.scheduler.stop()
        self.stop_process()


"""
This needs to be runnable from terminal as it runs in the background
"""
if __name__ == '__main__':
    bg_proc = background_process()
    bg_proc.start_process()