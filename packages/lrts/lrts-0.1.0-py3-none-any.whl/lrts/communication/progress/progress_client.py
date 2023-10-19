from abc import ABC, abstractmethod
from threading import Event
from typing import List

from lrts.communication.ipc_message import IPCMessage
from lrts.communication.progress.progress_client_information import ProgressClientInformation
from lrts.communication.router.progress_client_router import ProgressClientRouter


class ProgressClient(ABC):
    def __init__(self, client_information: ProgressClientInformation, router: ProgressClientRouter) -> None:
        self.client_information: ProgressClientInformation = client_information
        self.router: ProgressClientRouter = router

    @abstractmethod
    def start_client(self) -> None:
        """Start the progress client and connect to the progress server."""

    @abstractmethod
    def stop_client(self) -> None:
        """Stop the progress client and disconnect from the progress server."""

    @abstractmethod
    def get_approximate_rtt(self) -> float:
        """Return the current approximate RTT time from client to server."""

    @abstractmethod
    def get_unprocessed_ipc_messages(self) -> List[IPCMessage]:
        """Return all unprocessed IPC messages."""

    @abstractmethod
    def send_message_to_server(self, message: IPCMessage) -> None:
        """Send an IPCMessage to the progress server."""

    @abstractmethod
    def tick(self, stop_event: Event) -> None:
        """Process everything that happened between the last time this method was called and now.
        Do not process anything inside of tick if the stop_event has been set."""


if __name__ == '__main__':
    from lrts.communication.router.zmq_progress_client_router import ZMQProgressClientRouter
    from lrts.communication.progress.zmq_progress_client import ZMQProgressClient

    client_information: ProgressClientInformation = ProgressClientInformation(
        server_address="127.0.0.1",
        server_port="5454"
    )

    client_router: ProgressClientRouter = ZMQProgressClientRouter(client_information=client_information)
    client: ProgressClient = ZMQProgressClient(client_information=client_information, router=client_router)

    try:
        client.start_client()

        while True:
            pass
    except KeyboardInterrupt:
        print("Cleaning Up Client Resources...")  # ToDo: Implement custom logger interface
    finally:
        client.stop_client()
