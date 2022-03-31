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
 
### Public API
    def add_site(self, site_url):
        """
        Adds the url to the blocked lists
        """
        
        # Remove any http or www from site entry
        url = self.__fix_url(site_url)

        # Add the url to the hosts system
        self.__hosts.add(url)

        # Add the url to the config file
        ## TO_DO

    def remove_site(self, site_url):
        """
        Removes the url from the blocked lists
        """

        # Remove any http or www from site entry
        url = self.__fix_url(site_url)

        # Remove the url form the hosts system
        self.__hosts.remove(url)

        # Remove the url from the config file
        ## TO_DO

    def activate(self):
        """
        Activate the blocker with any permanent entries added to the hosts system.
        Also start the scheduler system to add and remove scheduled blocks at the right
        time.
        """

        # Save the current hosts lists, which also activates the 
        # hosts file on the system
        self.__hosts.save()

        # Activate the scheduler

    def disactivate(self):
        """
        Disactivate the blocker, removing all blocks including anything that has been 
        scheduled by the scheduling system. Cancel all scheduled blocks in the 
        scheduler system.
        """

        # Restore the hosts file to undo anyhting that has been applied to it
        self.__hosts.restore()

        # Disactive the scheduler

    def query_installed(self):
        """
        Returns a list of hosts the are installed on the system and in place 
        operating now
        """
        return self.__hosts.query()

    ## TO_DO
    def query_scheduled(self):
        """
        Returns a list of scheduled blocks and the times they are active
        """
        pass