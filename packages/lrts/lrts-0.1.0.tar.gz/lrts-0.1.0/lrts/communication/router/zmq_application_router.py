import pickle
from typing import Union, List

import zmq
from zmq import Context, Socket, Frame

from lrts.communication.application.application_information import ApplicationInformation
from lrts.communication.ipc_message import ApplicationConnectedIPCMessageData, ApplicationConnectedIPCMessage, \
    IPCMessageType, IPCMessage
from lrts.communication.router.application_router import ApplicationRouter
from lrts.communication.util.zmq_net_traffic_utils import zmq_net_traffic_to_ipc_messages


class ZMQApplicationRouter(ApplicationRouter):
    def __init__(self, application_information: ApplicationInformation) -> None:
        super().__init__(application_information=application_information)

        self._context: Union[Context, None] = None
        self._socket: Union[Socket, None] = None
        self._poller: zmq.Poller = zmq.Poller()

    def start_router(self) -> None:
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.DEALER)
        self._socket.setsockopt(zmq.IDENTITY, self.application_information.application_id.encode('utf-8'))
        self._socket.connect(
            f'tcp://{self.application_information.scheduler_address}:{self.application_information.scheduler_port}'
        )
        self._socket.RCVTIMEO = self.application_information.communication_time_out
        self._poller.register(self._socket, zmq.POLLIN)

        connected_data: ApplicationConnectedIPCMessageData = ApplicationConnectedIPCMessageData(
            application_information=self.application_information
        )
        connected_message: ApplicationConnectedIPCMessage = ApplicationConnectedIPCMessage(
            source_node_id=self.application_information.application_id,
            message_type=IPCMessageType.APPLICATION_CONNECTED,
            payload=connected_data
        )

        self.send_message_to_scheduler(message=connected_message)

        # ToDo: Implement custom logger interface
        print(f'Started application. '
              f'Connected to scheduler at: '
              f'{self.application_information.scheduler_address}:{self.application_information.scheduler_port}')

    def stop_router(self) -> None:
        if self._socket:
            self._poller.unregister(self._socket)
            self._socket.setsockopt(zmq.LINGER, 0)
            self._socket.close()
            self._socket = None

        if self._context:
            self._context.term()
            self._context = None

        print(f'Disconnected From Scheduler At: '
              f'{self.application_information.scheduler_address}:{self.application_information.scheduler_port}')

    def send_message_to_scheduler(self, message: IPCMessage) -> None:
        if self._socket is None:
            print("Failed To Send Message! Socket is null. Maybe you forgot to initialize the application?")
            print('application.start_application()')

        data_encoded: bytes = pickle.dumps(message)
        self._socket.send(data_encoded)

    def process_incoming_network_traffic(self) -> Union[List[IPCMessage], None]:
        try:
            traffic: List[Frame] | List[bytes] = self._socket.recv_multipart()
            return zmq_net_traffic_to_ipc_messages(traffic=traffic)
        except zmq.Again:
            pass

        return None
