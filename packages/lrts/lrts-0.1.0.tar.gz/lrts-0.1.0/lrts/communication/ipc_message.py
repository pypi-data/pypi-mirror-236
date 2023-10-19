from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import TypeAlias

from lrts.communication.application.application_information import ApplicationInformation
from lrts.communication.progress.progress_requests import ProgressCreateRequest, ProgressIncrementRequest, \
    ProgressCloseRequest
from lrts.communication.worker.worker_information import WorkerInformation


class IPCMessageType(Enum):
    APPLICATION_CONNECTED = "APPLICATION_CONNECTED"
    APPLICATION_START_SERVICE = "APPLICATION_START_SERVICE"
    APPLICATION_DISCONNECTED = "APPLICATION_DISCONNECTED"
    WORKER_CONNECTED = "WORKER_CONNECTED"
    WORKER_DISCONNECTED = "WORKER_DISCONNECTED"
    SCHEDULER_ACKNOWLEDGED_DISCONNECT = "SCHEDULER_ACKNOWLEDGED_DISCONNECT"
    WORKER_RESULT = "WORKER_RESULT"
    REQUEST_HEARTBEAT = "REQUEST_HEARTBEAT"
    REPLY_HEARTBEAT_WORKER = "REPLY_HEARTBEAT_WORKER"
    REPLY_HEARTBEAT_APPLICATION = "REPLY_HEARTBEAT_APPLICATION"
    PING = "PING"
    PONG = "PONG"
    SHUTDOWN_PROGRESS_CLIENT = "SHUTDOWN_PROGRESS_CLIENT"
    CREATE_PROGRESS = "CREATE_PROGRESS"
    INCREMENT_PROGRESS = "INCREMENT_PROGRESS"
    CLOSE_PROGRESS = "CLOSE_PROGRESS"


@dataclass
class IPCMessage:
    source_node_id: str
    message_type: IPCMessageType
    payload: IPCMessageData


@dataclass
class IPCMessageData:
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class WorkerConnectedIPCMessage(IPCMessage):
    payload: WorkerConnectedIPCMessageData


@dataclass
class WorkerConnectedIPCMessageData:
    worker_information: WorkerInformation


@dataclass
class ApplicationConnectedIPCMessage(IPCMessage):
    payload: ApplicationConnectedIPCMessageData


@dataclass
class ApplicationConnectedIPCMessageData:
    application_information: ApplicationInformation


@dataclass
class ApplicationDisconnectedIPCMessage(IPCMessage):
    payload: ApplicationDisconnectedIPCMessageData


@dataclass
class ApplicationDisconnectedIPCMessageData:
    application_information: ApplicationInformation


@dataclass
class WorkerDisconnectedIPCMessage(IPCMessage):
    payload: WorkerDisconnectedIPCMessageData


@dataclass
class WorkerDisconnectedIPCMessageData:
    worker_information: WorkerInformation


SchedulerAcknowledgedDisconnectIPCMessage: TypeAlias = IPCMessage
SchedulerAcknowledgedDisconnectIPCMessageData: TypeAlias = IPCMessageData

RequestHeartBeatIPCMessage: TypeAlias = IPCMessage
RequestHeartBeatIPCMessageData: TypeAlias = IPCMessageData


@dataclass
class ReplyHeartBeatWorkerIPCMessage(IPCMessage):
    payload: ReplyHeartBeatWorkerIPCMessageData


@dataclass
class ReplyHeartBeatWorkerIPCMessageData:
    worker_information: WorkerInformation


@dataclass
class ReplyHeartBeatApplicationIPCMessage(IPCMessage):
    payload: ReplyHeartBeatApplicationIPCMessageData


@dataclass
class ReplyHeartBeatApplicationIPCMessageData:
    application_information: ApplicationInformation


@dataclass
class StartServiceIPCMessage(IPCMessage):
    payload: StartServiceIPCMessageData


@dataclass
class StartServiceIPCMessageData:
    from lrts.service import Service

    service: Service
    application_id: str
    service_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class WorkerResultIPCMessage(IPCMessage):
    payload: WorkerResultIPCMessageData


@dataclass
class WorkerResultIPCMessageData:
    from lrts.service import ServiceResult

    service_result: ServiceResult
    service_id: str
    application_id: str


PingIPCMessage: TypeAlias = IPCMessage
PingIPCMessageData: TypeAlias = IPCMessageData

PongIPCMessage: TypeAlias = IPCMessage
PongIPCMessageData: TypeAlias = IPCMessageData

ShutdownProgressClientIPCMessage: TypeAlias = IPCMessage
ShutDownProgressClientIPCMessageData: TypeAlias = IPCMessageData


@dataclass
class CreateProgressIPCMessage(IPCMessage):
    payload: CreateProgressIPCMessageData


@dataclass
class CreateProgressIPCMessageData:
    create_info: ProgressCreateRequest


@dataclass
class IncrementProgressIPCMessage(IPCMessage):
    payload: IncrementProgressIPCMessageData


@dataclass
class IncrementProgressIPCMessageData:
    increment_info: ProgressIncrementRequest


@dataclass
class CloseProgressIPCMessage(IPCMessage):
    payload: CloseProgressIPCMessageData


@dataclass
class CloseProgressIPCMessageData:
    close_info: ProgressCloseRequest
