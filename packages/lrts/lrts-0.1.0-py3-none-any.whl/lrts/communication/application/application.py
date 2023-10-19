from abc import ABC, abstractmethod
from threading import Event
from typing import List, Generator, Union

from lrts.communication.application.application_information import ApplicationInformation
from lrts.communication.router.application_router import ApplicationRouter
from lrts.logging.logger import Logger
from lrts.service import ServiceResult, Service


class Application(ABC):
    def __init__(self, application_information: ApplicationInformation, router: ApplicationRouter,
                 logger: Union[Logger, None] = None) -> None:
        self.application_information: ApplicationInformation = application_information
        self.router: ApplicationRouter = router
        self.logger = logger

    @abstractmethod
    def start_application(self) -> None:
        """Start the application and all communication processes. Start listening to the scheduler for results."""

    @abstractmethod
    def stop_application(self) -> None:
        """Stop the application and all communication processes.
        Cleanup resources and ensure that the application could be restarted right now without issue.
        Notify the scheduler that you are going to disconnect and won't be submitting new work or requesting results."""

    @abstractmethod
    def schedule_service(self, service: Service) -> str:
        """Send service to scheduler. Return ID of the service."""

    @abstractmethod
    def tick(self, stop_event: Event) -> None:
        """Process everything that happened between the last time this method was called and now.
        Do not process anything inside of tick if the stop_event has been set."""

    @abstractmethod
    def wait_for(self, service_id: str) -> ServiceResult:
        """Return only when ServiceResult is ready."""

    @abstractmethod
    def wait_for_multi(self, service_ids: List[str]) -> List[ServiceResult]:
        """Return only when all ServiceResults are ready."""

    @abstractmethod
    def as_completed(self, service_ids: List[str]) -> Generator[ServiceResult, None, None]:
        """Generator, process results as they are completed."""


if __name__ == '__main__':
    from lrts.communication.router.zmq_application_router import ZMQApplicationRouter
    from lrts.communication.application.zmq_application import ZMQApplication

    application_information: ApplicationInformation = ApplicationInformation(
        scheduler_address='127.0.0.1',
        scheduler_port='5555',
        communication_time_out=1
    )
    application_router: ApplicationRouter = ZMQApplicationRouter(application_information=application_information)
    application: Application = ZMQApplication(
        application_information=application_information,
        router=application_router
    )

    try:
        application.start_application()

        while True:
            pass
    except KeyboardInterrupt:
        print("Cleaning Up Application Resources...")  # ToDo: Implement custom logger interface
    finally:
        application.stop_application()
