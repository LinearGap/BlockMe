
class config():
    """
    Class responsible for managing the config files for the application.
    Reading, writing, updating. Creation.
    """

    def __init__(self):
        # Config objects
        self.redirect_addr = '' # The ip address to use for redirection
        self.last_state = '' # The last state the application was in. Used to detect bad shutdown and reset before continuing
        self.scheduler_pid = 0 # The PID of the scheduler running process. To manage subprocess
        
        self.permanent_urls = [] # List of urls to be permanently blocked when the blocker runs
        self.scheduled_urls = [] # List of {'url':, 'start_time':, 'end_time':} dicts for scheduled blocking

    # Public API
    def load(self, config_path):
        """
        Load the config from the file at config_path.
        """
        pass

    def save(self, config_path):
        """
        Save the config to the file at config_path
        """
        pass

    def restore_default(self, config_path):
        """
        Restore the default config file to config_path
        """
        pass