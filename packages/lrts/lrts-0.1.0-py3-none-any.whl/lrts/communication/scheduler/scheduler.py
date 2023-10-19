from abc import ABC, abstractmethod
from threading import Event

from lrts.communication.router.scheduler_router import SchedulerRouter


class Scheduler(ABC):
    def __init__(self, router: SchedulerRouter) -> None:
        self._router: SchedulerRouter = router

    @abstractmethod
    def start_scheduler(self) -> None:
        """Initialize the scheduler, start the router, and begin accepting and distribution work."""

    @abstractmethod
    def stop_scheduler(self) -> None:
        """Alert workers to cancel running tasks,
        stop accepting and scheduling work / communications,
        cleanup all scheduler resources,
        ensure no lingering network binds so that the application would be free to restart again."""

    @abstractmethod
    def tick(self, stop_event: Event) -> None:
        """Process everything that has happened between the last time this method was called and now.
        Do not process anything inside of tick if the stop_event has been set."""


if __name__ == '__main__':
    from lrts.communication.router.zmq_scheduler_router import ZMQSchedulerRouter
    from lrts.communication.scheduler.zmq_scheduler import ZMQScheduler

    scheduler_router: SchedulerRouter = ZMQSchedulerRouter(bind_address='127.0.0.1',
                                                           bind_port='5555',
                                                           communication_time_out=1)

    scheduler: Scheduler = ZMQScheduler(router=scheduler_router)

    try:
        scheduler.start_scheduler()

        while True:
            pass
    except KeyboardInterrupt:
        print("Cleaning Up Scheduler Resources...")  # ToDo: Implement custom logger interface
    finally:
        scheduler.stop_scheduler()
