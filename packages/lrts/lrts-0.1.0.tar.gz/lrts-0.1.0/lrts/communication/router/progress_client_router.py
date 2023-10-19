from abc import ABC, abstractmethod
from typing import Union, List

from lrts.communication.ipc_message import IPCMessage
from lrts.communication.progress.progress_client_information import ProgressClientInformation


class ProgressClientRouter(ABC):
    def __init__(self, client_information: ProgressClientInformation) -> None:
        self.client_information: ProgressClientInformation = client_information

    @abstractmethod
    def start_router(self) -> None:
        """Initialize the client. Connect to server."""

    @abstractmethod
    def stop_router(self) -> None:
        """Stop the client. Disconnect from the server.
        Cleanup all resources so that the application could be restarted."""

    @abstractmethod
    def send_message_to_server(self, message: IPCMessage) -> None:
        """Send a message to the server router."""

    @abstractmethod
    def process_incoming_network_traffic(self) -> Union[List[IPCMessage], None]:
        """Return all IPC messages that have arrived since the last time this method was called."""
