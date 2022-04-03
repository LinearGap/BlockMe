from hosts import hosts as Hosts

class blocking():
    """
    Class responsible for blocking sites and where to redirect to
    adds and removes the blocked sites from all necessary places.
    """

    def __init__(self):
        self.__hosts = Hosts()

    def __fix_url(self, url):
        """
        Fix the url by removing any http or www leaving just 
        the domain entries
        """

        # Check for http or https
        protocol_stripped = ""        
        if url[:8] == 'https://':
            protocol_stripped = url[8:]
        elif url[:7] == 'http://':
            protocol_stripped = url[7:]
        else:
            # No protocol
            protocol_stripped = url

        # Check for www.
        domain = ""
        if protocol_stripped[:4] == 'www.':
            domain = protocol_stripped[4:]
        else:
            # No www
            domain = protocol_stripped


        return domain

    def __check_valid_ip(self, addr: str):
        """
        Checks if the addr supplied string is a valid ip address
        """
        octets = addr.split('.')
        if len(octets) != 4:
            return False

        for octet in octets:
            if not octet.isdigit():
                return False
            if int(octet) < 0 or int(octet) > 254:
                return False
        
        return True

    def __set_redirect_addr(self, addr: str):
        """
        Set a new redirect ip address in the hosts system
        """
        self.__hosts.redirect_ip_addr = addr
 
### Public API
    def add_site(self, site_url):
        """
        Adds the url to the blocked lists
        """
        
        # Remove any http or www from site entry
        url = self.__fix_url(site_url)

        # Add the url to the hosts system
        self.__hosts.add(url)


    def remove_site(self, site_url):
        """
        Removes the url from the blocked lists
        """

        # Remove any http or www from site entry
        url = self.__fix_url(site_url)

        # Remove the url form the hosts system
        self.__hosts.remove(url)


    def activate(self):
        """
        Active any currently added blocks on the system
        """

        # Save the current hosts lists, which also activates the 
        # hosts file on the system
        self.__hosts.save()

    def reactivate(self):
        """
        Reactive the blocks in the hosts system to update for added or removed url
        """

        # Save the current hosts lists, which also activates the 
        # hosts file on the system
        self.__hosts.save()

    def disactivate(self):
        """
        Disactivate the blocker, removing all blocks including anything that has been 
        scheduled by the scheduling system.
        """

        # Restore the hosts file to undo anyhting that has been applied to it
        self.__hosts.restore()


    def query_installed(self):
        """
        Returns a list of hosts the are installed on the system and in place 
        operating now
        """
        return self.__hosts.query()

    def set_redirect_address(self, addr: str):
        """
        Sets the redirection address to the supplied addr after checking if it
        is a valid ip address
        """
        if self.__check_valid_ip(addr):
            self.__set_redirect_addr(addr)

    def restore_default(self):
        """
        Restore to the system default hosts 
        """
        self.__hosts.restore()