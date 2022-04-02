from ast import arg
import sched
import time
import sched

class scheduler():
    """
    Class that is responsible for scheduling add and removing blocks
    with specified start and end times.
    """

    def __init__(self):  
        self.s = sched.scheduler(time.time, time.sleep)
        self.s.enter(10, 1, action=scheduler.boom, argument=(self, 'boom', ))
        self.s.enterabs(time.time()+5, 1, scheduler.boom, (self, 'abs boom',))
        self.s.run() 
        print("Scheduler running!!")

    def boom(self, pr):
        print(pr)


if __name__ == '__main__':
    s = scheduler()