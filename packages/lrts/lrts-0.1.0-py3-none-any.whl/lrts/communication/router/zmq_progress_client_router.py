import pickle
from typing import Union, List

import zmq
from zmq import Context, Socket, Frame

from lrts.communication.ipc_message import IPCMessage
from lrts.communication.progress.progress_client_information import ProgressClientInformation
from lrts.communication.router.progress_client_router import ProgressClientRouter
from lrts.communication.util.zmq_net_traffic_utils import zmq_net_traffic_to_ipc_messages


class ZMQProgressClientRouter(ProgressClientRouter):
    def __init__(self, client_information: ProgressClientInformation) -> None:
        super().__init__(client_information=client_information)

        self._context: Union[Context, None] = None
        self._socket: Union[Socket, None] = None
        self._poller: zmq.Poller = zmq.Poller()

    def start_router(self) -> None:
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.DEALER)
        self._socket.setsockopt(zmq.IDENTITY, self.client_information.node_id.encode('utf-8'))
        self._socket.connect(
            f'tcp://{self.client_information.server_address}:{self.client_information.server_port}'
        )
        self._socket.RCVTIMEO = self.client_information.communication_time_out
        self._poller.register(self._socket, zmq.POLLIN)

        # ToDo: Implement custom logger interface
        print(f'Started client. '
              f'Connected to server at: '
              f'{self.client_information.server_address}:{self.client_information.server_port}')

    def stop_router(self) -> None:
        if self._socket:
            self._poller.unregister(self._socket)
            self._socket.setsockopt(zmq.LINGER, 0)
            self._socket.close()
            self._socket = None

        if self._context:
            self._context.term()
            self._context = None

        print(f'Disconnected From Server At: '
              f'{self.client_information.server_address}:{self.client_information.server_port}')

    def send_message_to_server(self, message: IPCMessage) -> None:
        data_encoded: bytes = pickle.dumps(message)
        self._socket.send(data_encoded)

    def process_incoming_network_traffic(self) -> Union[List[IPCMessage], None]:
        try:
            traffic: List[Frame] | List[bytes] = self._socket.recv_multipart()
            return zmq_net_traffic_to_ipc_messages(traffic=traffic)
        except zmq.Again:
            pass

        return None
