from __future__ import annotations

import uuid
from dataclasses import dataclass
from multiprocessing import Pipe, Process
from threading import Event, Thread
from typing import Union, List, Generator, Dict, cast, Set
import time

from lrts.communication.application.application import Application
from lrts.communication.application.application_information import ApplicationInformation
from lrts.communication.ipc_message import ApplicationDisconnectedIPCMessageData, ApplicationDisconnectedIPCMessage, \
    IPCMessageType, IPCMessage, ReplyHeartBeatApplicationIPCMessageData, ReplyHeartBeatApplicationIPCMessage, \
    StartServiceIPCMessageData, StartServiceIPCMessage, WorkerResultIPCMessage, CreateProgressIPCMessage, \
    CloseProgressIPCMessage, IncrementProgressIPCMessage, ShutDownProgressClientIPCMessageData, \
    ShutdownProgressClientIPCMessage
from lrts.communication.progress.progress_client import ProgressClient
from lrts.communication.progress.progress_client_information import ProgressClientInformation
from lrts.communication.progress.progress_requests import ProgressCreateRequest, ProgressIncrementRequest, \
    ProgressCloseRequest
from lrts.communication.progress.zmq_progress_client import ZMQProgressClient
from lrts.communication.router.application_router import ApplicationRouter
from lrts.communication.router.progress_client_router import ProgressClientRouter
from lrts.communication.router.zmq_application_router import ZMQApplicationRouter
from lrts.communication.router.zmq_progress_client_router import ZMQProgressClientRouter
from lrts.logging.logger import Logger
from lrts.service import ServiceResult, Service


@dataclass
class ZMQApplicationSubprocess:
    process: Process
    pipe: Pipe


class ZMQApplication(Application):
    def __init__(self, application_information, router: Union[ApplicationRouter, None] = None,
                 logger: Union[Logger, None] = None) -> None:
        if router is None:
            router = ZMQApplication.default_router(application_information=application_information)

        super().__init__(application_information=application_information, router=router, logger=logger)

        self._stop_event: Event = Event()
        self._tick_thread: Union[Thread, None] = None

        self._progress_subprocess: Union[ZMQApplicationSubprocess, None] = None

        self._task_results: Dict[str, ServiceResult] = {}

    @staticmethod
    def default_router(application_information: ApplicationInformation) -> ApplicationRouter:
        application_router: ApplicationRouter = ZMQApplicationRouter(
            application_information=application_information
        )
        return application_router

    def start_progress_process(self) -> None:
        local_pipe, remote_pipe = Pipe()

        sub_process: Process = Process(
            target=ZMQApplication.progress_client_subprocess,
            args=(remote_pipe, self.application_information)
        )
        sub_process.start()

        progress_process_info: ZMQApplicationSubprocess = ZMQApplicationSubprocess(
            process=sub_process,
            pipe=local_pipe
        )

        self._progress_subprocess = progress_process_info

    def start_application(self) -> None:
        self.start_progress_process()
        self.router.start_router()

        self._tick_thread = Thread(target=self.tick, args=(self._stop_event,))
        self._tick_thread.start()

    def stop_application(self) -> None:
        shutdown_data: ShutDownProgressClientIPCMessageData = ShutDownProgressClientIPCMessageData()
        shutdown_message: ShutdownProgressClientIPCMessage = ShutdownProgressClientIPCMessage(
            source_node_id=self.application_information.application_id,
            message_type=IPCMessageType.SHUTDOWN_PROGRESS_CLIENT,
            payload=shutdown_data
        )
        self._progress_subprocess.pipe.send(shutdown_message)
        self._progress_subprocess.process.join()

        self._stop_event.set()
        if self._tick_thread is not None:
            self._tick_thread.join()

        self.router.stop_router()

    def schedule_service(self, service: Service) -> str:
        service_id: str = str(uuid.uuid4())

        start_service_data: StartServiceIPCMessageData = StartServiceIPCMessageData(
            service=service,
            application_id=self.application_information.application_id,
            service_id=service_id
        )
        start_service_message: StartServiceIPCMessage = StartServiceIPCMessage(
            source_node_id=self.application_information.application_id,
            message_type=IPCMessageType.APPLICATION_START_SERVICE,
            payload=start_service_data
        )

        self.router.send_message_to_scheduler(message=start_service_message)

        return service_id

    def handle_worker_completed_task(self, result_message: WorkerResultIPCMessage) -> None:
        service_id: str = result_message.payload.service_id
        result: ServiceResult = result_message.payload.service_result

        self._task_results[service_id] = result

    def wait_for(self, service_id: str) -> ServiceResult:
        while service_id not in self._task_results:
            pass

        result: ServiceResult = self._task_results[service_id]
        del self._task_results[service_id]

        return result

    def wait_for_multi(self, service_ids: List[str]) -> List[ServiceResult]:
        service_results: List[ServiceResult] = []
        removed_ids: List[str] = []

        while len(service_results) != len(service_ids):
            for service_id, service_result in list(self._task_results.items()):
                if service_id in service_ids:
                    service_results.append(service_result)
                    removed_ids.append(service_id)
                    del self._task_results[service_id]

        return service_results

    def as_completed(self, service_ids: List[str]) -> Generator[ServiceResult, None, None]:
        completed_ids: Set[str] = set()

        while len(completed_ids) != len(service_ids):
            for service_id, service_result in list(self._task_results.items()):
                if service_id in service_ids and service_id not in completed_ids:
                    yield service_result
                    completed_ids.add(service_id)
                    del self._task_results[service_id]

    def reply_heartbeat(self) -> None:
        if not self._stop_event.is_set():
            reply_data: ReplyHeartBeatApplicationIPCMessageData = ReplyHeartBeatApplicationIPCMessageData(
                application_information=self.application_information
            )
            reply_message: ReplyHeartBeatApplicationIPCMessage = ReplyHeartBeatApplicationIPCMessage(
                source_node_id=self.application_information.application_id,
                message_type=IPCMessageType.REPLY_HEARTBEAT_APPLICATION,
                payload=reply_data
            )

            self.router.send_message_to_scheduler(message=reply_message)

    @staticmethod
    def progress_client_subprocess(remote_pipe: Pipe, application_information: ApplicationInformation) -> None:
        client_information: ProgressClientInformation = ProgressClientInformation(
            server_address=application_information.progress_server_address,
            server_port=application_information.progress_server_port,
            progress_rtt_test_frequency=application_information.progress_rtt_test_frequency,
            node_id=application_information.application_id,
            communication_time_out=application_information.communication_time_out
        )

        client_router: ProgressClientRouter = ZMQProgressClientRouter(
            client_information=client_information
        )
        client: ProgressClient = ZMQProgressClient(
            client_information=client_information,
            router=client_router
        )
        client.start_client()

        try:
            should_shutdown: bool = False
            while not should_shutdown:
                new_messages: List[IPCMessage] = client.get_unprocessed_ipc_messages()

                if len(new_messages) > 0:
                    new_ipc_message: IPCMessage
                    for new_ipc_message in new_messages:
                        remote_pipe.send(new_ipc_message)

                if remote_pipe.poll():
                    message: IPCMessage = remote_pipe.recv()
                    message_type: IPCMessageType = message.message_type

                    match message_type:
                        case IPCMessageType.SHUTDOWN_PROGRESS_CLIENT:
                            should_shutdown = True
                        case _:
                            # ToDo: Custom Logging
                            print(f'Unhandled IPC Message Type In Progress Subprocess: {message_type}')
        except Exception as e:
            print(f'There was an error in the main progress client application loop: {e}')

        client.stop_client()

    def check_for_progress_updates(self) -> None:
        if self._progress_subprocess is None:
            return

        start_time_ms: float = time.time() * 1_000.00

        try:
            while self._progress_subprocess.pipe.poll():
                current_time_ms: float = time.time() * 1_000

                if current_time_ms - start_time_ms >= self.application_information.progress_iteration_timeout:
                    break

                next_ipc_message: IPCMessage = self._progress_subprocess.pipe.recv()
                message_type: IPCMessageType = next_ipc_message.message_type

                match message_type:
                    case IPCMessageType.CREATE_PROGRESS:
                        create_message: CreateProgressIPCMessage = cast(CreateProgressIPCMessage, next_ipc_message)
                        create_info: ProgressCreateRequest = create_message.payload.create_info

                        if self.logger is not None:
                            self.logger.create_counter(
                                total=create_info.total,
                                description=create_info.description,
                                unit=create_info.unit,
                                color=create_info.color,
                                leave=create_info.leave,
                                progress_id=create_info.progress_id
                            )
                    case IPCMessageType.INCREMENT_PROGRESS:
                        increment_message: IncrementProgressIPCMessage = cast(IncrementProgressIPCMessage, next_ipc_message)
                        increment_info: ProgressIncrementRequest = increment_message.payload.increment_info

                        if self.logger is not None:
                            self.logger.update_counter(progress_id=increment_info.progress_id, amount=increment_info.increment)
                    case IPCMessageType.CLOSE_PROGRESS:
                        close_message: CloseProgressIPCMessage = cast(CloseProgressIPCMessage, next_ipc_message)
                        close_info: ProgressCloseRequest = close_message.payload.close_info

                        if self.logger is not None:
                            self.logger.close_counter(progress_id=close_info.progress_id)
        except BrokenPipeError as _:
            pass

    def tick(self, stop_event: Event) -> None:
        disconnect_sent: bool = False
        disconnect_acknowledged: bool = False
        disconnect_start_time: float = 0

        while not disconnect_acknowledged:
            if stop_event.is_set() and not disconnect_sent:
                disconnected_data: ApplicationDisconnectedIPCMessageData = ApplicationDisconnectedIPCMessageData(
                    application_information=self.application_information
                )
                disconnected_message: ApplicationDisconnectedIPCMessage = ApplicationDisconnectedIPCMessage(
                    source_node_id=self.application_information.application_id,
                    message_type=IPCMessageType.APPLICATION_DISCONNECTED,
                    payload=disconnected_data
                )

                self.router.send_message_to_scheduler(message=disconnected_message)
                disconnect_sent = True
                disconnect_start_time = time.time()

            self.check_for_progress_updates()
            incoming_messages: Union[List[IPCMessage], None] = self.router.process_incoming_network_traffic()

            if not incoming_messages:
                if disconnect_sent and (time.time() - disconnect_start_time) * 1_000.00 > 10_000.00:
                    print("Scheduler failed to acknowledge disconnect. Exiting ungracefully.")
                    break

                continue

            for ipc_message in incoming_messages:
                ipc_message_type: IPCMessageType = ipc_message.message_type

                match ipc_message_type:
                    case IPCMessageType.REQUEST_HEARTBEAT:
                        self.reply_heartbeat()
                        break
                    case IPCMessageType.WORKER_RESULT:
                        self.handle_worker_completed_task(result_message=cast(WorkerResultIPCMessage, ipc_message))
                        break
                    case IPCMessageType.SCHEDULER_ACKNOWLEDGED_DISCONNECT:
                        disconnect_acknowledged = True
                        break
                    case _:
                        # ToDo: Implement custom logger interface
                        print(f'Unhandled IPC Message Type: {ipc_message_type}')
                        break
