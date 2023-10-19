from abc import ABC, abstractmethod
from typing import Union, List

from lrts.communication.ipc_message import IPCMessage
from lrts.communication.worker.worker_information import WorkerInformation


class WorkerRouter(ABC):
    def __init__(self, worker_information: WorkerInformation) -> None:
        self.worker_information: WorkerInformation = worker_information

    @abstractmethod
    def start_router(self) -> None:
        """Initialize the worker. Phone home to scheduler."""

    @abstractmethod
    def stop_router(self) -> None:
        """Stop the worker router and ensure that all resources are cleaned up so that application
        could safely restart."""

    @abstractmethod
    def send_message_to_scheduler(self, message: IPCMessage) -> None:
        """Send a message to the scheduler router."""

    @abstractmethod
    def process_incoming_network_traffic(self) -> Union[List[IPCMessage], None]:
        """Return all IPC messages that have arrived since the last time this method was called."""
