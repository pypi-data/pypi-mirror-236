import pickle
from typing import Union, List

import zmq
from zmq import Context, Socket, Frame

from lrts.communication.ipc_message import IPCMessage
from lrts.communication.router.progress_server_router import ProgressServerRouter
from lrts.communication.util.zmq_net_traffic_utils import zmq_net_traffic_to_ipc_messages


class ZMQProgressServerRouter(ProgressServerRouter):
    def __init__(self, bind_address: str, bind_port: str, communication_time_out: int = 1) -> None:
        super().__init__(bind_address=bind_address, bind_port=bind_port, communication_time_out=communication_time_out)

        self._context: Union[Context, None] = None
        self._socket: Union[Socket, None] = None
        self._poller: zmq.Poller = zmq.Poller()

    def start_router(self) -> None:
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.ROUTER)
        self._socket.bind(
            f'tcp://{self.bind_address}:{self.bind_port}'
        )
        self._socket.RCVTIMEO = self.communication_time_out
        self._poller.register(self._socket, zmq.POLLIN)

        print(f'Started Router At: {self.bind_address}:{self.bind_port}')  # ToDo: Implement custom logger interface

    def stop_router(self) -> None:
        if self._socket:
            self._poller.unregister(self._socket)
            self._socket.setsockopt(zmq.LINGER, 0)
            self._socket.close()
            self._socket = None

        if self._context:
            self._context.term()
            self._context = None

        print(f'Stopped Router At: {self.bind_address}:{self.bind_port}')  # ToDo: Implement Custom Logger Interface

    def send_message_to_node(self, node_id: str, message: IPCMessage) -> None:
        node_id_encoded: str = node_id.encode('utf-8')
        payload_encoded: bytes = pickle.dumps(message)

        self._socket.send_multipart([node_id_encoded,
                                     b'',
                                     payload_encoded])

    def process_incoming_network_traffic(self) -> Union[List[IPCMessage], None]:
        try:
            traffic: List[Frame] | List[bytes] = self._socket.recv_multipart()
            return zmq_net_traffic_to_ipc_messages(traffic=traffic)
        except zmq.Again:
            pass

        return None
