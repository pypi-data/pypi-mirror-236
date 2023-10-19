from __future__ import annotations
from abc import ABC, abstractmethod
from threading import Event

from lrts.communication.router.progress_server_router import ProgressServerRouter


class ProgressServer(ABC):
    def __init__(self, router: ProgressServerRouter) -> None:
        self.router: ProgressServerRouter = router

    @abstractmethod
    def start_server(self) -> None:
        """Initialize the progress server and start processing requests."""

    @abstractmethod
    def stop_server(self) -> None:
        """Shut down the progress server and stop processing new requests."""

    @abstractmethod
    def tick(self, stop_event: Event) -> None:
        """Process all requests that came between now and the last time this method was called."""


if __name__ == '__main__':
    from lrts.communication.router.zmq_progress_server_router import ZMQProgressServerRouter
    from lrts.communication.progress.zmq_progress_server import ZMQProgressServer

    progress_router: ProgressServerRouter = ZMQProgressServerRouter(
        bind_address='127.0.0.1',
        bind_port='5454',
        communication_time_out=1
    )

    progress_server: ProgressServer = ZMQProgressServer(router=progress_router)

    try:
        progress_server.start_server()

        while True:
            pass
    except KeyboardInterrupt:
        print("Cleaning Up Server Resources...")  # ToDo: Custom Logging
    finally:
        progress_server.stop_server()
