from multiprocessing import Event
from threading import Thread
from typing import Union, List, cast

from lrts.communication.ipc_message import IPCMessage, IPCMessageType, PingIPCMessage, PongIPCMessageData, \
    PongIPCMessage, CreateProgressIPCMessage, IncrementProgressIPCMessage, CloseProgressIPCMessage
from lrts.communication.progress.progress_server import ProgressServer
from lrts.communication.router.progress_server_router import ProgressServerRouter


class ZMQProgressServer(ProgressServer):
    def __init__(self, router: ProgressServerRouter) -> None:
        super().__init__(router=router)

        self._stop_event: Event = Event()
        self._tick_thread: Union[Thread, None] = None

    def start_server(self) -> None:
        self.router.start_router()

        self._tick_thread: Thread = Thread(target=self.tick, args=(self._stop_event,))
        self._tick_thread.start()

    def stop_server(self) -> None:
        self._stop_event.set()
        if self._tick_thread is not None:
            self._tick_thread.join()

        self.router.stop_router()

    def handle_ping(self, ping_message: PingIPCMessage) -> None:
        source_node_id: str = ping_message.source_node_id

        pong_data: PongIPCMessageData = PongIPCMessageData()
        pong_message: PongIPCMessage = PongIPCMessage(
            source_node_id="SERVER",
            message_type=IPCMessageType.PONG,
            payload=pong_data
        )

        self.router.send_message_to_node(node_id=source_node_id, message=pong_message)

    def forward_create_message(self, message: CreateProgressIPCMessage) -> None:
        application_id: str = message.payload.create_info.application_id
        self.router.send_message_to_node(node_id=application_id, message=message)

    def forward_increment_message(self, message: IncrementProgressIPCMessage) -> None:
        application_id: str = message.payload.increment_info.application_id
        self.router.send_message_to_node(node_id=application_id, message=message)

    def forward_close_message(self, message: CloseProgressIPCMessage) -> None:
        application_id: str = message.payload.close_info.application_id
        self.router.send_message_to_node(node_id=application_id, message=message)

    def tick(self, stop_event: Event) -> None:
        while not stop_event.is_set():
            incoming_messages: Union[List[IPCMessage], None] = self.router.process_incoming_network_traffic()

            if not incoming_messages:
                continue

            for ipc_message in incoming_messages:
                ipc_message_type: IPCMessageType = ipc_message.message_type

                match ipc_message_type:
                    case IPCMessageType.PING:
                        self.handle_ping(ping_message=cast(PingIPCMessage, ipc_message))
                    case IPCMessageType.CREATE_PROGRESS:
                        self.forward_create_message(message=cast(CreateProgressIPCMessage, ipc_message))
                    case IPCMessageType.INCREMENT_PROGRESS:
                        self.forward_increment_message(message=cast(IncrementProgressIPCMessage, ipc_message))
                    case IPCMessageType.CLOSE_PROGRESS:
                        self.forward_close_message(message=cast(CloseProgressIPCMessage, ipc_message))
                    case _:
                        # ToDo: Implement custom logger interface
                        print(f'Unhandled IPC Message Type: {ipc_message_type}')
