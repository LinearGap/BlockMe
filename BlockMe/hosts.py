import platform

class hosts:
    """
    Class responsible for interacting with the hosts file on the 
    operating system
    """

    # The path to the hosts file on each OS
    path = {'Linux': '/etc/hosts', 
            'Darwin': '/etc/hosts',
            'Windows': 'c:\windows\system32\drivers\etc\hosts'}

    def __init__(self):
        self.__filepath = hosts.path[self.__get_os()]
        self.__backup_filepath = self.__filepath + '_BACKUP'

    def __get_os(self):
        """
        Get the name of the current system OS
        Returns: system name
        """
        system = platform.system()
        return system

    def __read_file(self, filepath):
        """
        Read the file on the system and return it as a list
        """
        hosts_file_contents = []
        hosts_file = open(filepath, 'r')
        with hosts_file:
            hosts_file_contents = hosts_file.readlines()
        
        return hosts_file_contents

    def __write_file(self, filepath, contents):
        """
        Write the supplied contents into a file. Replaces anyhting currently 
        there. Does not append.
        """
        hosts_file = open(filepath, 'w+')
        with hosts_file:
            hosts_file_contents = hosts_file.writelines(contents)

    def read_current(self):
        try:
            return self.__read_file(self.__filepath)
        except:
            return None

    def read_backup(self):
        try:
            return self.__read_file(self.__backup_filepath)
        except:
            return None

    def write_backup(self):
        """
        Replace this
        """
        h = self.read_current()
        self.__write_file(self.__backup_filepath, h)
        