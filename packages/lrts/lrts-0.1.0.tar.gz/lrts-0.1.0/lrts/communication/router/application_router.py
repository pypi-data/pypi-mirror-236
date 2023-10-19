from abc import ABC, abstractmethod
from typing import Union, List

from lrts.communication.application.application_information import ApplicationInformation
from lrts.communication.ipc_message import IPCMessage


class ApplicationRouter(ABC):
    def __init__(self, application_information: ApplicationInformation) -> None:
        self.application_information: ApplicationInformation = application_information

    @abstractmethod
    def start_router(self) -> None:
        """Initialize the application. Phone home to the scheduler."""

    @abstractmethod
    def stop_router(self) -> None:
        """Stop the application and ensure that all resources are cleaned up so that the application could safely
        restart."""

    @abstractmethod
    def send_message_to_scheduler(self, message: IPCMessage) -> None:
        """Send a message to the scheduler router."""

    @abstractmethod
    def process_incoming_network_traffic(self) -> Union[List[IPCMessage], None]:
        """Return all IPC messages that have arrived since the last time this method was called."""
