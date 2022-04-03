import time
import sched
from config import config
from blocking import blocking

class scheduler_process():
    """
    Class that is responsible for being the background process that manages
    schedules and keeps itself running indefinetly.

    This will be started by the scheduler and not launched directly
    """

    def __init__(self, config: config, blocker: blocking):
        """
        Wait for 10 seconds before doing anything to allow other process to
        finish
        """
        time.sleep(10)

        # Get the config, supplied by running process
        self.__conf = config
        # Get the blocker supplied by running process
        self.__blocker = blocker

        # Perform setup actions
        self.__perform_setup()

        # Setup scheduler
        self.__scheduler = sched.scheduler(time.time, time.sleep)

        # Print message to show fully running
        #print("BlockMe background process running.")

        self.__events = [] # List of events

        self.stop_signal = False
        self.midnight = False

    def __perform_setup(self):
        """
        Perform any setup actions for the scheduler to be running
        """
        pass

    def __main_loop(self):
        """
        The loop that keeps the scheduler running
        """
        #while not self.stop_signal:
        self.midnight = False
        self.__add_events()
        self.__add_master_event()
        self.__scheduler.run(blocking=False)

        while not self.midnight:
            # Sleep for a minute then check again if anything needs to happen
            time.sleep(10)
            self.__scheduler.run(blocking=False)


    def __add_events(self):
        """
        Adds the events to the scheduler for all scheduled times
        """
        for scheduled in self.__conf.scheduled_urls:
            
            # Has the end time already passed?
            if self.__is_strtime_passed(scheduled['end_time']):
                self.__remove_block_now(scheduled['url'])
                continue

            # Has start time already passed?
            elif self.__is_strtime_passed(scheduled['start_time']):
                self.__add_block_now(scheduled['url'])
                self.__add_end_event(scheduled['end_time'], scheduled['url'])

            # Add event to the scheduler with this url and start and end times
            else:
                self.__add_start_event(scheduled['start_time'], scheduled['url'])
                self.__add_end_event(scheduled['end_time'], scheduled['url'])

    def __add_master_event(self):
        """
        Adds an event for midnight that clears all running events and
        starts the daily process again.
        """
        now = time.localtime(time.time())

        midnight = (24, 0)
        secs_until = self.__get_seconds_until(midnight)
        e_id = self.__scheduler.enterabs(time.time() + secs_until, 1, scheduler_process.__midnight_reset, argument=(self))
        self.__events.append(e_id)


    def time_to_tuple(self, strtime):
        """
        Convert from a 'HH:MM' time string to a (hour: HH, minute: MM) tuple
        """
        hour = int(strtime[0:2])
        minutes = int(strtime[-2:])
        time_tuple = (hour, minutes)

        return time_tuple


    def __is_strtime_passed(self, strtime):
        """
        Check if string in format "HH:MM" has already passed for today
        """
        time_tuple = self.time_to_tuple(strtime)
        hour = time_tuple[0]
        minutes = time_tuple[1]

        now = time.localtime(time.time())

        if hour < now.tm_hour:
            # Hour is before current time therefore time has elapsed
            return True

        if hour == now.tm_hour:
            # Same hour, check if minutes is less
            if minutes <= now.tm_min:
                return True

        return False


    def __add_block_now(self, url):
        """
        Adds a blocked site to the blocked system straight away. Used when
        the time for start has already passed
        """
        self.__blocker.add_site(url)
        self.__blocker.reactivate()

    def __remove_block_now(self, url):
        """
        Removes a blocked site from the blocked system straight away. Used when end
        time has aldready passed.
        """
        self.__blocker.remove_site(url)
        # Activate the blocker to reset what is currently being blocked
        self.__blocker.reactivate()

    def __get_seconds_until(self, time_until):
        """
        Get the time in seconds between now and then
        time_until = (hours, minutes)
        """
        now = time.localtime(time.time())
        hours_diff = time_until[0] - now.tm_hour
        mins_diff = time_until[1] - now.tm_min
        seconds = ((hours_diff * 60) * 60) + (mins_diff * 60)  

        return seconds

    def __add_start_event(self, time_at, url):
        """
        Add an event for the specified time and url. For starting blocks
        """
        time_tuple = self.time_to_tuple(time_at)
        secs_until = self.__get_seconds_until(time_tuple)

        e_id = self.__scheduler.enterabs(time.time() + secs_until, 3, scheduler_process.__add_block_now, argument=(self, url))
        self.__events.append(e_id)

    def __add_end_event(self, time_at, url):
        """
        Add an event for the specified time and url. For ending blocks
        """
        time_tuple = self.time_to_tuple(time_at)
        secs_until = self.__get_seconds_until(time_tuple)

        e_id = self.__scheduler.enterabs(time.time() + secs_until, 3, scheduler_process.__remove_block_now, argument=(self, url))
        self.__events.append(e_id)

    def __midnight_reset(self):
        """
        Clear all events ready for the day to begin again
        """
        for e in self.__events:
            try:
                self.__scheduler.cancel(e)
            except:
                pass

        self.__events.clear()
        self.midnight = True


# Public API

    def start(self):
        """
        Start the scheduler process and loops
        """
        # Run the main loop
        while not self.stop_signal:
            self.__main_loop()

    def stop(self):
        """
        Stop the scheduler process immediately
        """
        self.__midnight_reset()
        self.stop_signal = True