import pickle
from typing import Union, List

import zmq
from zmq import Context, Socket, Frame

from lrts.communication.ipc_message import WorkerConnectedIPCMessageData, WorkerConnectedIPCMessage, IPCMessage, \
    IPCMessageType
from lrts.communication.router.worker_router import WorkerRouter
from lrts.communication.util.zmq_net_traffic_utils import zmq_net_traffic_to_ipc_messages
from lrts.communication.worker.worker import WorkerInformation


class ZMQWorkerRouter(WorkerRouter):
    def __init__(self, worker_information: WorkerInformation) -> None:
        super().__init__(worker_information=worker_information)

        self._context: Union[Context, None] = None
        self._socket: Union[Socket, None] = None
        self._poller: zmq.Poller = zmq.Poller()

    def start_router(self) -> None:
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.DEALER)
        self._socket.setsockopt(zmq.IDENTITY, self.worker_information.node_id.encode('utf-8'))
        self._socket.connect(
            f'tcp://{self.worker_information.scheduler_address}:{self.worker_information.scheduler_port}'
        )
        self._socket.RCVTIMEO = self.worker_information.communication_time_out
        self._poller.register(self._socket, zmq.POLLIN)

        connected_data: WorkerConnectedIPCMessageData = WorkerConnectedIPCMessageData(
            worker_information=self.worker_information
        )
        connected_message: WorkerConnectedIPCMessage = WorkerConnectedIPCMessage(
            source_node_id=self.worker_information.node_id,
            message_type=IPCMessageType.WORKER_CONNECTED,
            payload=connected_data
        )

        self.send_message_to_scheduler(message=connected_message)

        # ToDo: Implement custom logger interface
        print(f'Started worker. '
              f'Connected to scheduler at: '
              f'{self.worker_information.scheduler_address}:{self.worker_information.scheduler_port}')

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
              f'{self.worker_information.scheduler_address}:{self.worker_information.scheduler_port}')

    def send_message_to_scheduler(self, message: IPCMessage) -> None:
        data_encoded: bytes = pickle.dumps(message)
        self._socket.send(data_encoded)

    def process_incoming_network_traffic(self) -> Union[List[IPCMessage], None]:
        try:
            traffic: List[Frame] | List[bytes] = self._socket.recv_multipart()
            return zmq_net_traffic_to_ipc_messages(traffic=traffic)
        except zmq.Again:
            pass

        return None
