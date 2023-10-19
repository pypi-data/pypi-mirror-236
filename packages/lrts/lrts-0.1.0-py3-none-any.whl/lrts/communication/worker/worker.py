from abc import ABC, abstractmethod
from threading import Event

from lrts.communication.router.worker_router import WorkerRouter
from lrts.communication.worker.worker_information import WorkerInformation


class Worker(ABC):
    def __init__(self, worker_information: WorkerInformation, router: WorkerRouter) -> None:
        self.worker_information: WorkerInformation = worker_information
        self.router: WorkerRouter = router

    @abstractmethod
    def start_worker(self) -> None:
        """Start the worker and all communication processes. Start listening to the scheduler
        and be ready to accept work."""

    @abstractmethod
    def stop_worker(self) -> None:
        """Stop the worker and all communication processes.
        Cleanup resources and ensure that the application could be restarted right now without issue.
        Notify the scheduler that you are going to disconnect, cancel all remaining work,
        and no longer accept new work."""

    @abstractmethod
    def tick(self, stop_event: Event) -> None:
        """Process everything that happened between the last time this method was called and now.
        Do not process anything inside of tick if the stop_event has been set."""


if __name__ == '__main__':
    from lrts.communication.router.zmq_worker_router import ZMQWorkerRouter
    from lrts.communication.worker.zmq_worker import ZMQWorker

    worker_information: WorkerInformation = WorkerInformation(
        scheduler_address='127.0.0.1',
        scheduler_port='5555',
        progress_server_address='127.0.0.1',
        progress_server_port='5454',
        max_simultaneous_jobs=2,
        communication_time_out=1
    )
    worker_router: WorkerRouter = ZMQWorkerRouter(worker_information=worker_information)

    worker: Worker = ZMQWorker(worker_information=worker_information, router=worker_router)

    try:
        worker.start_worker()

        while True:
            pass
    except KeyboardInterrupt:
        print("Cleaning Up Worker Resources...")  # ToDo: Implement custom logger interface
    finally:
        worker.stop_worker()
