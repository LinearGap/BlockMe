from datetime import datetime
from appdirs import user_config_dir
from config_default import config as default_config
import os, shutil, json

class config():
    """
    Class responsible for managing the config files for the application.
    Reading, writing, updating. Creation.
    """

    def __init__(self):
        # Config objects
        self.redirect_addr = '' # The ip address to use for redirection
        self.__redirect_addr_name = 'redirrect_addr' # Name to use in JSON In/Out
        self.last_state = '' # The last state the application was in. Used to detect bad shutdown and reset before continuing
        self.__last_state_name = 'last_state'  # Name to use in JSON In/Out
        self.scheduler_pid = 0 # The PID of the scheduler running process. To manage subprocess
        self.__scheduler_pid_name = 'scheduler_pid'  # Name to use in JSON In/Out
        
        self.permanent_urls = [] # List of urls to be permanently blocked when the blocker runs
        self.__permanent_urls_name = 'permanent_urls' # Name to use in JSON In/Out
        self.scheduled_urls = [] # List of {'url':, 'start_time':, 'end_time':} dicts for scheduled blocking
        self.__scheduled_urls_name = 'scheduled_urls' # Name to use in JSON In/Out

        # Config directory platform specific
        self.__config_dir = user_config_dir('BlockMe.PY')
        self.__config_filepath = self.__config_dir + '/BlockMe.cfg'

        # Check for config file, directory and write default config if needed
        if not self.__check_config_dir():
            self.__create_config_dir()
            self.__copy_defaut_config()

    def __check_config_dir(self):
        """
        Checks if the config directory exists
        """
        return os.path.isdir(self.__config_dir)
    
    def __create_config_dir(self):
        """
        Creates the config directory
        """
        try:
            os.mkdir(self.__config_dir)
            return
        except:
            # Handle error, directory already exists so just return
            return

    def __copy_defaut_config(self):
        """
        Copies the default config to the config directory on the system
        """
        try:
            file = open(self.__config_filepath, 'w')
            with file:
                file.write(default_config)
        except:
            raise

    def __delete_config_file(self):
        """
        Delete the current config file if needing a reset
        """
        try:
            os.remove(self.__config_filepath)
        except:
            return

    def __read_config_file(self):
        """
        Read and return the raw data from the config filepath. 
        Only use after checking the file acually exists
        """

        f = open(self.__config_filepath, 'r')
        with f:
            raw_data = f.read()

        return raw_data

    def __decode_json(self, raw_json):
        """
        Decodes the raw json string into a json object
        """
        try:
            json_data = json.loads(raw_json)
            return json_data
        except:
            print("Bad config file! Unable to decode JSON")
            return

    def __json_to_vars(self, json_data: dict):
        """
        Takes the decoded json object parses it for correctness,
        and updates config variables
        """
        self.redirect_addr = json_data.get(self.__redirect_addr_name, '127.0.0.1')
        self.last_state = json_data.get(self.__last_state_name, 0)
        self.scheduler_pid = json_data.get(self.__scheduler_pid_name, 0)

        # For lists check that all entries are valid
        for item in json_data.get(self.__permanent_urls_name, []):
            if type(item) is str:
                self.permanent_urls.append(item)

        for item in json_data.get(self.__scheduled_urls_name, []):
            # Check each dict contains the keys needed to be valid
            if 'url' in item.keys() and 'start_time' in item.keys() and 'end_time' in item.keys():
                self.scheduled_urls.append(item)

    def __build_json_output(self):
        """
        Take the config vars and turn into a json object that can be written out
        """
        raw_obj = {}
        raw_obj['Updated'] = datetime.ctime(datetime.now()) # Add an updated timestamp to the output
        raw_obj[self.__last_state_name] = self.last_state
        raw_obj[self.__redirect_addr_name] = self.redirect_addr
        raw_obj[self.__scheduler_pid_name] = self.scheduler_pid

        raw_obj[self.__permanent_urls_name] = self.permanent_urls
        raw_obj[self.__scheduled_urls_name] = self.scheduled_urls

        return json.dumps(raw_obj, indent=2)

    def __write_json_config_file(self, json_data):
        """
        Write the JSON to the config file
        """
        try:
            f = open(self.__config_filepath, 'w')
            with f:
                f.write(json_data)
        except:
            return


# Public API
    def load(self):
        """
        Load the config from the file at config_path.
        """
        try:
            data = self.__read_config_file()
            json_data = self.__decode_json(data)
            self.__json_to_vars(json_data)
            return True
        except:
            return False


    def save(self):
        """
        Save the config to the file at config_path
        """
        data = self.__build_json_output()
        self.__write_json_config_file(data)

    def restore_default(self):
        """
        Restore the default config file to config_path
        """
        if self.__check_config_dir():
            # If directory doesn't exist then need to create it first
            self.__delete_config_file()
            self.__copy_defaut_config
        else:
            self.__create_config_dir()
            self.__copy_defaut_config()