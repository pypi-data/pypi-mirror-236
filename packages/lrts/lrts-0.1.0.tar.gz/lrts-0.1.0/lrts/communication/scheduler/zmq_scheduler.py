from dataclasses import dataclass, field
from typing import Union, List, cast, Dict
from threading import Event, Thread
import time

from lrts.communication.application.application_information import ApplicationInformation
from lrts.communication.ipc_message import IPCMessage, IPCMessageType, WorkerConnectedIPCMessage, \
    WorkerDisconnectedIPCMessage, SchedulerAcknowledgedDisconnectIPCMessageData, \
    SchedulerAcknowledgedDisconnectIPCMessage, RequestHeartBeatIPCMessageData, RequestHeartBeatIPCMessage, \
    ReplyHeartBeatWorkerIPCMessage, ApplicationConnectedIPCMessage, ApplicationDisconnectedIPCMessage, \
    ReplyHeartBeatApplicationIPCMessage, StartServiceIPCMessage, WorkerResultIPCMessage
from lrts.communication.router.scheduler_router import SchedulerRouter
from lrts.communication.scheduler.scheduler import Scheduler
from lrts.communication.worker.worker_information import WorkerInformation


# ToDo: Need to reschedule service when worker is disconnected while it has a
#       currently running task


@dataclass
class ZMQWorkerInformation:
    worker_information: WorkerInformation
    last_heartbeat_sent: float
    last_heartbeat_received: float
    active_jobs: int = field(default_factory=lambda: 0)


@dataclass
class ZMQApplicationInformation:
    application_information: ApplicationInformation
    last_heartbeat_sent: float
    last_heartbeat_received: float


class ZMQScheduler(Scheduler):
    def __init__(self, router: SchedulerRouter) -> None:
        super().__init__(router=router)

        self._stop_event: Event = Event()
        self._tick_thread: Union[Thread, None] = None
        self._heartbeat_thread: Union[Thread, None] = None

        self._applications: Dict[str, ZMQApplicationInformation] = {}
        self._workers: Dict[str, ZMQWorkerInformation] = {}
        self._worker_active_tasks: Dict[str, List[StartServiceIPCMessage]] = {}
        self._queued_tasks: List[StartServiceIPCMessage] = []

        # ToDo: Should be in some config / env variable
        self._scheduler_send_heartbeat_frequency_ms: float = 30_000.00
        self._scheduler_heartbeat_timeout_ms: float = 60_000.00

    def start_scheduler(self) -> None:
        self._router.start_router()

        self._tick_thread = Thread(target=self.tick, args=(self._stop_event,))
        self._tick_thread.start()

        self._heartbeat_thread = Thread(target=self.heartbeat_tasks, args=(self._stop_event,))
        self._heartbeat_thread.start()

    def stop_scheduler(self) -> None:
        self._stop_event.set()
        if self._tick_thread is not None:
            self._tick_thread.join()

        self._router.stop_router()

    def handle_worker_connected(self, message: WorkerConnectedIPCMessage) -> None:
        worker_id: str = message.payload.worker_information.node_id
        worker_information: WorkerInformation = message.payload.worker_information

        current_time_ms: float = time.time() * 1_000.00

        if worker_id not in self._workers:
            self._workers[worker_id] = ZMQWorkerInformation(
                worker_information=worker_information,
                last_heartbeat_sent=current_time_ms,
                last_heartbeat_received=current_time_ms
            )
        else:
            self._workers[worker_id].worker_information = worker_information
            self._workers[worker_id].last_heartbeat_sent = current_time_ms
            self._workers[worker_id].last_heartbeat_received = current_time_ms

            # ToDo: Implement custom logger interface
            print(f'Worker with ID: {worker_id} connected, but a worker with this ID already exists!')
            return

        # ToDo: Implement custom logger interface
        print(f'Worker with ID: {worker_id} connected!')

    def handle_worker_disconnected(self, message: WorkerDisconnectedIPCMessage) -> None:
        acknowledge_disconnect_data: SchedulerAcknowledgedDisconnectIPCMessageData = \
            SchedulerAcknowledgedDisconnectIPCMessageData()

        acknowledge_disconnect_message: SchedulerAcknowledgedDisconnectIPCMessage = \
            SchedulerAcknowledgedDisconnectIPCMessage(
                source_node_id='SCHEDULER',
                message_type=IPCMessageType.SCHEDULER_ACKNOWLEDGED_DISCONNECT,
                payload=acknowledge_disconnect_data
            )

        self._router.send_message_to_worker(
            message=acknowledge_disconnect_message,
            worker_id=message.payload.worker_information.node_id
        )

        rescheduled_tasks: int = 0

        if message.payload.worker_information.node_id in self._workers:
            worker_id: str = message.payload.worker_information.node_id

            if worker_id in self._worker_active_tasks:
                worker_active_tasks: List[StartServiceIPCMessage] = self._worker_active_tasks[worker_id]

                task: StartServiceIPCMessage
                for task in worker_active_tasks:
                    self._queued_tasks.append(task)
                    rescheduled_tasks += 1

                del self._worker_active_tasks[worker_id]

            del self._workers[worker_id]
        else:
            # ToDo: Implement custom logger interface
            print(f'Worker with ID: {message.payload.worker_information.node_id} '
                  f'requested disconnect but was previously disconnected. Likely timed out previously.')

        # ToDo: Implement custom logger interface
        print(f'Worker with ID: {message.payload.worker_information.node_id} disconnected. '
              f'Rescheduled {rescheduled_tasks} uncompleted tasks!')

    def handle_application_connected(self, message: ApplicationConnectedIPCMessage) -> None:
        application_id: str = message.payload.application_information.application_id
        application_information: ApplicationInformation = message.payload.application_information

        current_time_ms: float = time.time() * 1_000.00

        if application_id not in self._applications:
            self._applications[application_id] = ZMQApplicationInformation(
                application_information=application_information,
                last_heartbeat_sent=current_time_ms,
                last_heartbeat_received=current_time_ms
            )
        else:
            self._applications[application_id].application_information = application_information
            self._applications[application_id].last_heartbeat_sent = current_time_ms
            self._applications[application_id].last_heartbeat_received = current_time_ms

            # ToDo: Implement custom logger interface
            print(f'Application with ID: {application_id} connected, but an application with this ID already exists!')
            return

        # ToDo: Implement custom logger interface
        print(f'Application with ID: {application_id} connected!')

    def handle_application_disconnected(self, message: ApplicationDisconnectedIPCMessage) -> None:
        acknowledge_disconnect_data: SchedulerAcknowledgedDisconnectIPCMessageData = \
            SchedulerAcknowledgedDisconnectIPCMessageData()

        acknowledge_disconnect_message: SchedulerAcknowledgedDisconnectIPCMessage = \
            SchedulerAcknowledgedDisconnectIPCMessage(
                source_node_id='SCHEDULER',
                message_type=IPCMessageType.SCHEDULER_ACKNOWLEDGED_DISCONNECT,
                payload=acknowledge_disconnect_data
            )

        self._router.send_message_to_worker(
            message=acknowledge_disconnect_message,
            worker_id=message.payload.application_information.application_id
        )

        if message.payload.application_information.application_id in self._applications:
            self.remove_application(application_id=message.payload.application_information.application_id)
        else:
            # ToDo: Implement custom logger interface
            print(f'Application with ID: {message.payload.application_information.application_id} '
                  f'requested disconnect but was previously disconnected. Likely timed out previously.')

        # ToDo: Implement custom logger interface
        print(f'Application with ID: {message.payload.application_information.application_id} disconnected!')

    def remove_application(self, application_id: str) -> None:
        if application_id in self._applications:
            del self._applications[application_id]

    def try_reset_worker_and_handle_unreachable(self, worker_id: str) -> None:
        if worker_id in self._worker_active_tasks:
            worker_active_tasks: List[StartServiceIPCMessage] = self._worker_active_tasks[worker_id]

            task: StartServiceIPCMessage
            for task in worker_active_tasks:
                self._queued_tasks.append(task)

            del self._worker_active_tasks[worker_id]

        if worker_id in self._workers:
            del self._workers[worker_id]
        else:
            # ToDo: Implement custom logger interface
            print(f'Trying to reset worker with ID: {worker_id} but no worker with that ID exists locally.')

    def handle_unknown_worker_order_reset_reconnect(self, network_node_id: str) -> None:
        print(f'Unknown node with ID: {network_node_id}. Attempting to order reset/reconnect.')
        # ToDo: Handle
        pass

    def handle_receive_worker_heartbeat(self, message: ReplyHeartBeatWorkerIPCMessage) -> None:
        worker_id: str = message.payload.worker_information.node_id

        if worker_id in self._workers:
            current_time_ms: float = time.time() * 1_000.00

            self._workers[worker_id].last_heartbeat_received = current_time_ms
            self._workers[worker_id].worker_information = message.payload.worker_information
        else:
            # ToDo: Implement custom logger interface
            # ToDo: Send worker an IPC message ordering it to stop, reset and reconnect
            self.handle_unknown_worker_order_reset_reconnect(network_node_id=worker_id)
            print(f'Worker with ID: {message.payload.worker_information.node_id} '
                  f'replied with a heartbeat but is not a connected worker? '
                  f'Likely worker previously incorrectly disconnected or timed out.')

    def handle_receive_application_heartbeat(self, message: ReplyHeartBeatApplicationIPCMessage) -> None:
        application_id: str = message.payload.application_information.application_id

        if application_id in self._applications:
            current_time_ms: float = time.time() * 1_000.00

            self._applications[application_id].last_heartbeat_received = current_time_ms
            self._applications[application_id].application_information = message.payload.application_information
        else:
            self.remove_application(application_id=application_id)
            # ToDo: Implement custom logger interface
            print(f'Application with ID: {message.payload.application_information.application_id} '
                  f'replied with a heartbeat but is not a connected application? '
                  f'Likely application previously incorrectly disconnected or timed out.')

    def request_worker_heartbeats(self) -> None:
        current_time_ms: float = time.time() * 1_000.00

        for worker_id, worker in self._workers.items():
            time_since_last_heartbeat = current_time_ms - worker.last_heartbeat_sent

            if time_since_last_heartbeat > self._scheduler_send_heartbeat_frequency_ms:
                heartbeat_data: RequestHeartBeatIPCMessageData = RequestHeartBeatIPCMessageData()
                heartbeat_message: RequestHeartBeatIPCMessage = RequestHeartBeatIPCMessage(
                    source_node_id='SCHEDULER',
                    message_type=IPCMessageType.REQUEST_HEARTBEAT,
                    payload=heartbeat_data
                )

                self._router.send_message_to_worker(
                    worker_id=worker_id,
                    message=heartbeat_message,
                )

                worker.last_heartbeat_sent = current_time_ms

    def request_application_heartbeats(self) -> None:
        current_time_ms: float = time.time() * 1_000.00

        for application_id, application in self._applications.items():
            time_since_last_heartbeat: float = current_time_ms - application.last_heartbeat_sent

            if time_since_last_heartbeat > self._scheduler_send_heartbeat_frequency_ms:
                heartbeat_data: RequestHeartBeatIPCMessageData = RequestHeartBeatIPCMessageData()
                heartbeat_message: RequestHeartBeatIPCMessage = RequestHeartBeatIPCMessage(
                    source_node_id="SCHEDULER",
                    message_type=IPCMessageType.REQUEST_HEARTBEAT,
                    payload=heartbeat_data
                )

                self._router.send_message_to_worker(
                    worker_id=application_id,
                    message=heartbeat_message
                )

                application.last_heartbeat_sent = current_time_ms

    def handle_worker_time_outs(self) -> None:
        current_time_ms: float = time.time() * 1_000.00

        workers_to_reset: List[str] = []

        for worker_id, worker in self._workers.items():
            time_since_last_worker_reply: float = current_time_ms - worker.last_heartbeat_received

            if time_since_last_worker_reply > self._scheduler_heartbeat_timeout_ms:
                workers_to_reset.append(worker_id)

        for worker_id_to_reset in workers_to_reset:
            # ToDo: Implement custom logger interface
            print(f'Worker with ID: {worker_id_to_reset} disconnected due to heartbeat timeout.')
            self.try_reset_worker_and_handle_unreachable(worker_id=worker_id_to_reset)

    def handle_application_time_outs(self) -> None:
        current_time_ms: float = time.time() * 1_000.00

        applications_to_purge: List[str] = []

        for application_id, application in self._applications.items():
            time_since_last_application_reply: float = current_time_ms - application.last_heartbeat_received

            if time_since_last_application_reply > self._scheduler_heartbeat_timeout_ms:
                applications_to_purge.append(application_id)

        for application_id_to_purge in applications_to_purge:
            # ToDo: Implement custom logger interface
            print(f'Application with ID: {application_id_to_purge} disconnected due to heartbeat timeout.')
            self.remove_application(application_id=application_id_to_purge)

    def heartbeat_tasks(self, stop_event: Event) -> None:
        while not stop_event.is_set():
            self.request_worker_heartbeats()
            self.handle_worker_time_outs()

            self.request_application_heartbeats()
            self.handle_application_time_outs()

            time.sleep(self._scheduler_send_heartbeat_frequency_ms / 1_000.00)

    def send_task_to_worker(self, worker_id: str, request_data: StartServiceIPCMessage) -> None:
        self._router.send_message_to_worker(
            worker_id=worker_id,
            message=request_data
        )

        self._workers[worker_id].active_jobs += 1

        if worker_id not in self._worker_active_tasks:
            self._worker_active_tasks[worker_id] = [request_data]
            return

        self._worker_active_tasks[worker_id].append(request_data)

    def handle_application_start_service(self, request_data: StartServiceIPCMessage) -> None:
        print("APPLICATION REQUESTED SERVICE TO START")

        found_free_worker: bool = False

        for worker_id, worker in self._workers.items():
            worker_max_jobs: int = worker.worker_information.max_simultaneous_jobs
            worker_current_jobs: int = worker.active_jobs

            if worker_current_jobs < worker_max_jobs:
                self.send_task_to_worker(worker_id=worker_id, request_data=request_data)
                found_free_worker = True
                break

        if not found_free_worker:
            self._queued_tasks.append(request_data)

    def try_schedule_tasks(self) -> None:
        unmatched_tasks: List[StartServiceIPCMessage] = []
        available_workers = set(self._workers.keys())

        for task in self._queued_tasks:
            worker_assigned = False

            for worker_id in list(available_workers):
                worker = self._workers[worker_id]
                worker_max_jobs = worker.worker_information.max_simultaneous_jobs
                worker_current_jobs = worker.active_jobs

                if worker_current_jobs < worker_max_jobs:
                    self.send_task_to_worker(worker_id=worker_id, request_data=task)
                    if worker_current_jobs + 1 >= worker_max_jobs:
                        available_workers.remove(worker_id)
                    worker_assigned = True
                    break

            if not worker_assigned:
                unmatched_tasks.append(task)

        self._queued_tasks = unmatched_tasks

    def handle_worker_completed_task(self, result_message: WorkerResultIPCMessage) -> None:
        print("SCH RECEIVED WORKER RESULT")

        worker_id: str = result_message.source_node_id
        application_id: str = result_message.payload.application_id
        service_id: str = result_message.payload.service_id

        self._router.send_message_to_worker(
            worker_id=application_id,
            message=result_message
        )

        worker_active_tasks: List[StartServiceIPCMessage] = self._worker_active_tasks[worker_id]
        worker_unfinished_tasks: List[StartServiceIPCMessage] = []

        task: StartServiceIPCMessage
        for task in worker_active_tasks:
            if task.payload.service_id != service_id:
                worker_unfinished_tasks.append(task)

        self._worker_active_tasks[worker_id] = worker_unfinished_tasks

        if worker_id in self._workers:
            self._workers[result_message.source_node_id].active_jobs -= 1
        else:
            print("An unregistered worker submitted a task for completion!")

    def tick(self, stop_event: Event) -> None:
        while not stop_event.is_set():
            incoming_messages: Union[List[IPCMessage], None] = self._router.process_incoming_network_traffic()

            self.request_worker_heartbeats()
            self.handle_worker_time_outs()
            self.try_schedule_tasks()

            if not incoming_messages:
                continue

            for ipc_message in incoming_messages:
                ipc_message_type: IPCMessageType = ipc_message.message_type

                match ipc_message_type:
                    case IPCMessageType.REPLY_HEARTBEAT_WORKER:
                        self.handle_receive_worker_heartbeat(message=cast(ReplyHeartBeatWorkerIPCMessage, ipc_message))
                        break
                    case IPCMessageType.REPLY_HEARTBEAT_APPLICATION:
                        self.handle_receive_application_heartbeat(
                            message=cast(
                                ReplyHeartBeatApplicationIPCMessage,
                                ipc_message
                            )
                        )
                        break
                    case IPCMessageType.WORKER_RESULT:
                        self.handle_worker_completed_task(result_message=cast(WorkerResultIPCMessage, ipc_message))
                        break
                    case IPCMessageType.APPLICATION_START_SERVICE:
                        self.handle_application_start_service(request_data=cast(StartServiceIPCMessage, ipc_message))
                        break
                    case IPCMessageType.WORKER_CONNECTED:
                        self.handle_worker_connected(message=cast(WorkerConnectedIPCMessage, ipc_message))
                        break
                    case IPCMessageType.APPLICATION_CONNECTED:
                        self.handle_application_connected(message=cast(ApplicationConnectedIPCMessage, ipc_message))
                        break
                    case IPCMessageType.WORKER_DISCONNECTED:
                        self.handle_worker_disconnected(message=cast(WorkerDisconnectedIPCMessage, ipc_message))
                        break
                    case IPCMessageType.APPLICATION_DISCONNECTED:
                        self.handle_application_disconnected(message=cast(ApplicationDisconnectedIPCMessage, ipc_message))
                        break
                    case _:
                        # ToDo: Implement custom logger interface
                        print(f'Unhandled IPC Message Type: {ipc_message_type}')
