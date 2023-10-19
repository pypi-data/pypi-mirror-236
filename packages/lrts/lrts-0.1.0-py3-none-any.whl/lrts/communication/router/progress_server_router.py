from abc import ABC, abstractmethod
from typing import Union, List

from lrts.communication.ipc_message import IPCMessage


class ProgressServerRouter(ABC):
    def __init__(self, bind_address: str, bind_port: str, communication_time_out: int = 1) -> None:
        self.bind_address: str = bind_address
        self.bind_port: str = bind_port
        self.communication_time_out: int = communication_time_out

    @abstractmethod
    def start_router(self) -> None:
        """Initialize the router and bind to the target 'bind_address', 'bind_port' that was passed into the
        constructor. Start accepting traffic."""

    @abstractmethod
    def stop_router(self) -> None:
        """Cleanup router resources and ensure all addresses and ports are unbound so the application would be
        free to restart again without issue."""

    @abstractmethod
    def send_message_to_node(self, node_id: str, message: IPCMessage) -> None:
        """Send an IPC message to the designated node."""

    @abstractmethod
    def process_incoming_network_traffic(self) -> Union[List[IPCMessage], None]:
        """Process and return all incoming network traffic that has been received since the
        last time this method was called."""
