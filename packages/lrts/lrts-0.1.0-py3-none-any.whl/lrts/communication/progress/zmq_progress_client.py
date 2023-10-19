import time
from threading import Event, Thread
from typing import Union, List

from lrts.communication.ipc_message import IPCMessage, IPCMessageType, PingIPCMessageData, PingIPCMessage
from lrts.communication.progress.progress_client import ProgressClient
from lrts.communication.progress.progress_client_information import ProgressClientInformation
from lrts.communication.router.progress_client_router import ProgressClientRouter


# ToDo: Maybe get rid of the ping pong RTT test and replace it by adding headers to IPCMessages with default
#       fields that include the time the message was sent.


class ZMQProgressClient(ProgressClient):
    def __init__(self, client_information: ProgressClientInformation, router: ProgressClientRouter) -> None:
        super().__init__(client_information=client_information, router=router)

        self._stop_event: Event = Event()
        self._tick_thread: Union[Thread, None] = None

        self._is_waiting_rtt_test: bool = False
        self._last_rtt_test: float = (time.time() * 1_000.00) - client_information.progress_rtt_test_frequency
        self._approximate_rtt: float = 0.0

        self._unprocessed_messages: List[IPCMessage] = []

    def start_client(self) -> None:
        self.router.start_router()

        self._tick_thread: Thread = Thread(target=self.tick, args=(self._stop_event,))
        self._tick_thread.start()

    def stop_client(self) -> None:
        self._stop_event.set()
        if self._tick_thread is not None:
            self._tick_thread.join()

        self.router.stop_router()

    def send_rtt_test(self) -> None:
        if self._is_waiting_rtt_test:
            return

        self._is_waiting_rtt_test = True

        current_time_ms: float = time.time() * 1_000.00
        self._last_rtt_test = current_time_ms

        ping_data: PingIPCMessageData = PingIPCMessageData()
        ping_message: PingIPCMessage = PingIPCMessage(
            source_node_id=self.client_information.node_id,
            message_type=IPCMessageType.PING,
            payload=ping_data
        )

        self.router.send_message_to_server(message=ping_message)

    def handle_pong(self) -> None:
        current_time_ms: float = time.time() * 1_000.00
        self._is_waiting_rtt_test = False

        self._approximate_rtt = current_time_ms - self._last_rtt_test

    def get_approximate_rtt(self) -> float:
        approximate_rtt: float = self._approximate_rtt

        if approximate_rtt <= 0:
            return 120.00

        if approximate_rtt >= 10_000:
            return 10_000.00

        return approximate_rtt

    def send_message_to_server(self, message: IPCMessage) -> None:
        self.router.send_message_to_server(message=message)

    def get_unprocessed_ipc_messages(self) -> List[IPCMessage]:
        messages: List[IPCMessage] = list(self._unprocessed_messages)
        self._unprocessed_messages.clear()

        return messages

    def tick(self, stop_event: Event) -> None:
        while not stop_event.is_set():
            current_time_ms: float = time.time() * 1_000.00

            if current_time_ms - self._last_rtt_test >= self.client_information.progress_rtt_test_frequency:
                self.send_rtt_test()

            incoming_messages: Union[List[IPCMessage], None] = self.router.process_incoming_network_traffic()

            if not incoming_messages:
                continue

            ipc_message: IPCMessage
            for ipc_message in incoming_messages:
                ipc_message_type: IPCMessageType = ipc_message.message_type

                match ipc_message_type:
                    case IPCMessageType.PONG:
                        self.handle_pong()
                    case IPCMessageType.CREATE_PROGRESS:
                        self._unprocessed_messages.append(ipc_message)
                    case IPCMessageType.INCREMENT_PROGRESS:
                        self._unprocessed_messages.append(ipc_message)
                    case IPCMessageType.CLOSE_PROGRESS:
                        self._unprocessed_messages.append(ipc_message)
                    case _:
                        # ToDo: Implement custom logger interface
                        print(f'Unhandled IPC Message Type: {ipc_message_type}')
