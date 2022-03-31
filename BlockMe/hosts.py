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

    # The header to write in host file above any added hosts
    header = '# BlockMe hosts. Run BlockMe stop to remove'

    # The footer after the hosts have been added
    footer = '# End of BlockME hosts.'

    # The IP address to use as a redirect
    ip_redirect = '127.0.0.1'

    def __init__(self):
        # Setup config variables to be editable from external using
        # defaults of hosts
        self.entry_header = hosts.header
        self.entry_footer = hosts.footer
        self.redirect_ip_addr = hosts.ip_redirect

        # Paths of the files on this system        
        self.__hosts_filepath = hosts.path[self.__get_os()]
        self.__hosts_backup_filepath = self.__hosts_filepath + '.bmb'
        self.__first_run_master_backup_filepath = self.__hosts_filepath + '_FRMB.bmb'

        # List of sites to block when writing the hosts file
        self.__blocked_hosts = []

        # Read the current hosts file and save into backup file and
        # also into system_hosts for use later
        self.__system_hosts = self.__read_current_hosts()
        self.__write_backup_hosts(self.__system_hosts)

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
        Write the supplied contents into a file. Replaces anything currently 
        there. Does not append.
        """
        hosts_file = open(filepath, 'w+')
        with hosts_file:
            hosts_file_contents = hosts_file.writelines(contents)

    def __read_current_hosts(self):
        try:
            return self.__read_file(self.__hosts_filepath)
        except:
            return None

    def __read_backup_hosts(self):
        try:
            return self.__read_file(self.__hosts_backup_filepath)
        except:
            return None

    def __write_backup_hosts(self, contents):
        """
        Write the supplied contents into the backup hosts file
        """
        try:
            self.__write_file(self.__hosts_backup_filepath, contents)
        except:
            raise

    def __write_first_run_master_backup_hosts(self, contents):
        """
        Write the supplied contents into the first run master backup
        hosts file. Only to be used on first run of the programm
        """
        try:
            self.__write_file(self.__write_first_run_master_backup_hosts, contents)
        except:
            raise

    def __format_hosts(self):
        """
        Creates an output list for saving to hosts appending header
        and footer into the output along with the current hosts file
        """
        output = []
        try:
            output.extend(self.__system_hosts)
            output.append('\n##\n')
            output.append(hosts.header + '\n')
            output.append('#\n')
            # Loop through the blocked address list and create string to append to the list
            for addr in self.__blocked_hosts:
                line = hosts.ip_redirect + ' ' + addr + '\n'
                output.append(line)
            output.append('#\n')
            output.append(hosts.footer + '\n')
            output.append('##\n')
        except:
            raise

        return output

    def __get_curent_blocked_in_hosts_file(self):
        """
        Returns a list of what is currently blocked from the hosts file by
        this. Only includes what is between the header and footer
        """

        # Loop through the system hosts
        inside_added = False # Have we found what we are looking for
        added_hosts = [] # List of what we have added
        for line in self.__read_current_hosts():

            # strip new line characters otherwise comparison will fail
            if line.strip('#').strip('\n') == hosts.header.strip('#').strip('\n'):
                inside_added = True
                continue
            
            # If were inside the header, check this isn't the footer
            if inside_added and line == self.entry_footer:
                # No need to keep looking
                inside_added = False
                break

            # Ignore any commented line
            if inside_added and line[0] == '#':
                continue
            
            # Read the line
            if inside_added:
                # Split the line into its parts
                parts = line.split(' ')
                # Part 2 would be the domain
                added_hosts.append(parts[1].strip('\n'))
                continue

        return added_hosts



    ### Public API

    def get(self):
        """
        Returns the list of hosts store in the blocked hosts lists
        does not return anything from the system. Only what is managed
        by this script
        """
        return self.__blocked_hosts

    def add(self, *addr):
        """
        Adds the address: addr to the blocked hosts list 
        """
        for address in addr:
            self.__blocked_hosts.append(address)

    def add_list(self, addr_list):
        """
        Adds the supplied list of hosts to the blocked hosts list
        """
        self.__blocked_hosts.extend(addr_list)

    def remove(self, addr):
        """
        Remove the addr from the blocked hosts lists,
        addr could be in blocked hosts more than once so,
        loop until this is not the fact
        """
        while(addr in self.__blocked_hosts):
            self.__blocked_hosts.remove(addr)

    def remove_list(self, addr_list):
        """
        Remove the addr in list from the blocked hosts lists,
        addr could be in blocked hosts more than once so,
        loop until this is not the fact
        """
        for addr in addr_list:
            self.remove(addr)
        
    def save(self):
        """
        Saves the contents of the blocked hosts lists along with the header
        and footer into the hosts file on the system
        """
        try:
            self.__write_file(self.__hosts_filepath, self.__format_hosts())
        except:
            raise

    def restore(self):
        """
        Restores the hosts file to the system state from before anything 
        was written to it
        """
        backup = self.__read_backup_hosts()
        self.__write_file(self.__hosts_filepath, backup)

    def query(self):
        """
        Return a list of currently blocked hosts that have been installed
        by this system between the header and the footer
        """
        return self.__get_curent_blocked_in_hosts_file()
        