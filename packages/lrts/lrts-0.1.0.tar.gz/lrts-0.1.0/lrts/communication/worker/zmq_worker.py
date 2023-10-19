from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from multiprocessing import Queue, Process, Pipe
from typing import Union, List, Dict, cast
from threading import Event, Thread
import time

from lrts.communication.ipc_message import WorkerDisconnectedIPCMessageData, WorkerDisconnectedIPCMessage, \
    IPCMessageType, IPCMessage, ReplyHeartBeatWorkerIPCMessageData, ReplyHeartBeatWorkerIPCMessage, \
    StartServiceIPCMessage, WorkerResultIPCMessageData, WorkerResultIPCMessage, ShutDownProgressClientIPCMessageData, \
    ShutdownProgressClientIPCMessage, CreateProgressIPCMessage, CloseProgressIPCMessage, IncrementProgressIPCMessage
from lrts.communication.progress.progress_client import ProgressClient
from lrts.communication.progress.progress_client_information import ProgressClientInformation
from lrts.communication.progress.progress_requests import ProgressIncrementRequest, ProgressCreateRequest, \
    ProgressCloseRequest
from lrts.communication.progress.zmq_progress_client import ZMQProgressClient
from lrts.communication.router.progress_client_router import ProgressClientRouter
from lrts.communication.router.worker_router import WorkerRouter
from lrts.communication.router.zmq_progress_client_router import ZMQProgressClientRouter
from lrts.communication.worker.worker import Worker, WorkerInformation
from lrts.service import Service, ServiceResult


@dataclass
class ZMQWorkerServiceProcess:
    service_id: str
    process: Process
    service: Service
    original_message: StartServiceIPCMessage
    queue: Queue
    result: Union[ServiceResult, None] = field(default_factory=lambda: None)


@dataclass
class ZMQWorkerProgressService:
    process: Union[Process, None]
    local_pipe: Pipe


class ZMQWorker(Worker):
    def __init__(self, worker_information: WorkerInformation, router: WorkerRouter) -> None:
        super().__init__(worker_information=worker_information, router=router)

        self._stop_event: Event = Event()
        self._tick_thread: Union[Thread, None] = None

        self._active_tasks: Dict[str, ZMQWorkerServiceProcess] = {}

    def start_worker(self) -> None:
        self.router.start_router()

        self._tick_thread = Thread(target=self.tick, args=(self._stop_event,))
        self._tick_thread.start()

    def stop_worker(self) -> None:
        # ToDo: Should kill all running task processes

        self._stop_event.set()
        if self._tick_thread is not None:
            self._tick_thread.join()

        self.router.stop_router()

    def reply_heartbeat(self) -> None:
        if not self._stop_event.is_set():
            reply_data: ReplyHeartBeatWorkerIPCMessageData = ReplyHeartBeatWorkerIPCMessageData(
                worker_information=self.worker_information
            )
            reply_message: ReplyHeartBeatWorkerIPCMessage = ReplyHeartBeatWorkerIPCMessage(
                source_node_id=self.worker_information.node_id,
                message_type=IPCMessageType.REPLY_HEARTBEAT_WORKER,
                payload=reply_data
            )

            self.router.send_message_to_scheduler(message=reply_message)

    def begin_work(self, request_data: StartServiceIPCMessage) -> None:
        service: Service = request_data.payload.service
        service_id: str = request_data.payload.service_id

        if service_id in self._active_tasks:
            raise Exception(f'Service with ID: {service_id} already exists! Critical Error!')  # ToDo: Custom Logging

        result_queue: Queue = Queue()

        service_process = Process(
            target=ZMQWorker.service_subprocess,
            args=(service, service_id, result_queue, self.worker_information, request_data.payload.application_id)
        )
        service_process.start()

        worker_task_information: ZMQWorkerServiceProcess = ZMQWorkerServiceProcess(
            service_id=service_id,
            process=service_process,
            service=service,
            original_message=request_data,
            queue=result_queue
        )

        self._active_tasks[service_id] = worker_task_information

    def check_active_tasks_for_completion(self) -> None:
        finished_services: Dict[str, ZMQWorkerServiceProcess] = {}

        service_id: str
        service_info: ZMQWorkerServiceProcess
        for service_id, service_info in self._active_tasks.items():
            if not service_info.process.is_alive():
                service_result: ServiceResult = service_info.queue.get()

                service_info.queue.close()
                service_info.process.join()

                service_info.result = service_result

                finished_services[service_result.service_id] = service_info

        service_id: str
        service_info: ZMQWorkerServiceProcess
        for service_id, service_info in finished_services.items():
            result_message_data: WorkerResultIPCMessageData = WorkerResultIPCMessageData(
                service_result=service_info.result,
                service_id=service_info.service_id,
                application_id=service_info.original_message.payload.application_id
            )
            result_message: WorkerResultIPCMessage = WorkerResultIPCMessage(
                source_node_id=self.worker_information.node_id,
                message_type=IPCMessageType.WORKER_RESULT,
                payload=result_message_data
            )

            self.router.send_message_to_scheduler(message=result_message)

            del self._active_tasks[service_id]

    @staticmethod
    def service_subprocess(service: Service, service_id: str, queue: Queue,
                           worker_information: WorkerInformation, application_id: str) -> None:
        local_pipe, remote_pipe = Pipe()
        sub_process: Process = Process(
            target=ZMQWorker.progress_client_subprocess,
            args=(remote_pipe, worker_information)
        )
        sub_process.start()

        progress_process_info: ZMQWorkerProgressService = ZMQWorkerProgressService(
            process=sub_process,
            local_pipe=local_pipe
        )

        result: ServiceResult = service.worker_begin_service(service_id=service_id, service=service,
                                                             progress_ipc_pipe=local_pipe,
                                                             application_id=application_id)

        shutdown_client_data: ShutDownProgressClientIPCMessageData = ShutDownProgressClientIPCMessageData()
        shutdown_client_message: ShutdownProgressClientIPCMessage = ShutdownProgressClientIPCMessage(
            source_node_id=worker_information.node_id,
            message_type=IPCMessageType.SHUTDOWN_PROGRESS_CLIENT,
            payload=shutdown_client_data
        )
        progress_process_info.local_pipe.send(shutdown_client_message)

        progress_process_info.process.join()

        queue.put(result)

    @staticmethod
    def progress_client_subprocess(remote_pipe: Pipe, worker_information: WorkerInformation) -> None:
        create_queue: Dict[str, CreateProgressIPCMessage] = {}
        close_queue: Dict[str, CloseProgressIPCMessage] = {}
        increment_queue: Dict[str, IncrementProgressIPCMessage] = {}

        last_batch_sent_time: float = time.time() * 1_000.00

        client_information: ProgressClientInformation = ProgressClientInformation(
            server_address=worker_information.progress_server_address,
            server_port=worker_information.progress_server_port,
            node_id=str(uuid.uuid4()),  # ToDo: Might be better to use service_id here instead of random generated
            communication_time_out=worker_information.communication_time_out,
            progress_rtt_test_frequency=worker_information.progress_rtt_test_frequency
        )

        client_router: ProgressClientRouter = ZMQProgressClientRouter(client_information=client_information)
        client: ProgressClient = ZMQProgressClient(
            client_information=client_information,
            router=client_router
        )
        client.start_client()

        try:
            should_shutdown: bool = False
            while not should_shutdown:
                current_time_ms: float = time.time() * 1_000.00
                approximate_rtt: float = client.get_approximate_rtt()
                time_since_last_batch: float = current_time_ms - last_batch_sent_time

                total_queue_len: int = len(increment_queue) + len(create_queue) + len(close_queue)

                if time_since_last_batch >= approximate_rtt and total_queue_len > 0:
                    last_batch_sent_time = current_time_ms

                    # ToDo: These should all be bundled into a single object and sent to be
                    #  unwrapped on the application

                    create_request: CreateProgressIPCMessage
                    for _, create_request in create_queue.items():
                        client.send_message_to_server(message=create_request)

                    increment_request: IncrementProgressIPCMessage
                    for _, increment_request in increment_queue.items():
                        client.send_message_to_server(message=increment_request)

                    close_request: CloseProgressIPCMessage
                    for _, close_request in close_queue.items():
                        client.send_message_to_server(message=close_request)

                    create_queue.clear()
                    increment_queue.clear()
                    close_queue.clear()

                if remote_pipe.poll():
                    message: IPCMessage = remote_pipe.recv()
                    message_type: IPCMessageType = message.message_type

                    match message_type:
                        case IPCMessageType.SHUTDOWN_PROGRESS_CLIENT:
                            should_shutdown = True
                        case IPCMessageType.CREATE_PROGRESS:
                            create_message: CreateProgressIPCMessage = cast(CreateProgressIPCMessage, message)
                            create_queue[create_message.payload.create_info.progress_id] = create_message
                        case IPCMessageType.CLOSE_PROGRESS:
                            close_message: CloseProgressIPCMessage = cast(CloseProgressIPCMessage, message)
                            progress_id: str = close_message.payload.close_info.progress_id

                            # This progress bar never even left the worker, just kill it
                            if progress_id in create_queue:
                                del create_queue[progress_id]
                                if progress_id in increment_queue:
                                    del increment_queue[progress_id]
                            # Clear any pending increments as the bar is about to close
                            elif progress_id in increment_queue:
                                del increment_queue[progress_id]

                            close_queue[progress_id] = close_message
                        case IPCMessageType.INCREMENT_PROGRESS:
                            increment_message: IncrementProgressIPCMessage = cast(IncrementProgressIPCMessage, message)
                            progress_id: str = increment_message.payload.increment_info.progress_id

                            # The progress is buffered to close so don't bother incrementing
                            if progress_id in close_queue:
                                pass
                            # There are already requests to increment this progress in the buffer
                            elif progress_id in increment_queue:
                                increment_queue[progress_id].payload.increment_info.increment += \
                                    increment_message.payload.increment_info.increment
                            else:
                                increment_queue[progress_id] = increment_message

                        case _:
                            # ToDo: Custom Logging
                            print(f'Unhandled IPC Message Type In Progress Subprocess: {message_type}')
        except Exception as e:
            print(f'Error in main progress worker loop: {e}')

        client.stop_client()

    def tick(self, stop_event: Event) -> None:
        disconnect_sent: bool = False
        disconnect_acknowledged: bool = False
        disconnect_start_time: float = 0

        while not disconnect_acknowledged:
            if stop_event.is_set() and not disconnect_sent:
                disconnected_data: WorkerDisconnectedIPCMessageData = WorkerDisconnectedIPCMessageData(
                    worker_information=self.worker_information
                )
                disconnected_message: WorkerDisconnectedIPCMessage = WorkerDisconnectedIPCMessage(
                    source_node_id=self.worker_information.node_id,
                    message_type=IPCMessageType.WORKER_DISCONNECTED,
                    payload=disconnected_data
                )

                self.router.send_message_to_scheduler(message=disconnected_message)
                disconnect_sent = True
                disconnect_start_time = time.time()

            self.check_active_tasks_for_completion()

            incoming_messages: Union[List[IPCMessage], None] = self.router.process_incoming_network_traffic()

            if not incoming_messages:
                if disconnect_sent and (time.time() - disconnect_start_time) * 1000 > 10_000:
                    print("Scheduler failed to acknowledge disconnect. Exiting ungracefully.")
                    break

                continue

            for ipc_message in incoming_messages:
                ipc_message_type: IPCMessageType = ipc_message.message_type

                match ipc_message_type:
                    case IPCMessageType.APPLICATION_START_SERVICE:
                        self.begin_work(request_data=cast(StartServiceIPCMessage, ipc_message))
                        break
                    case IPCMessageType.REQUEST_HEARTBEAT:
                        self.reply_heartbeat()
                        break
                    case IPCMessageType.SCHEDULER_ACKNOWLEDGED_DISCONNECT:
                        disconnect_acknowledged = True
                        break
                    case _:
                        # ToDo: Implement custom logger interface
                        print(f'Unhandled IPC Message Type: {ipc_message_type}')
                        break
