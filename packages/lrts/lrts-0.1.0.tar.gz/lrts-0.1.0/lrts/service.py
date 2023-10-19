from __future__ import annotations

import traceback
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from multiprocessing import Pipe
from typing import Union, Any


class ServiceResultStatus(Enum):
    PENDING = "PENDING"
    FINISHED = "FINISHED"
    CRASHED = "CRASHED"


@dataclass
class ServiceResult:
    service_id: str
    service_status: ServiceResultStatus = field(default_factory=lambda: ServiceResultStatus.PENDING)
    service_result: Union[Any, None] = field(default_factory=lambda: None)


class Service(ABC):
    def __init__(self) -> None:
        self._service_id: Union[str, None] = None
        self._progress_ipc_pipe: Union[Pipe, None] = None
        self._application_id: Union[str, None] = None

    def create_progress(self, description: str, color: str, total: int, leave: bool, unit: str) -> str:
        progress_id: str = str(uuid.uuid4())

        from lrts.communication.progress.progress_requests import ProgressCreateRequest
        from lrts.communication.ipc_message import CreateProgressIPCMessageData
        from lrts.communication.ipc_message import CreateProgressIPCMessage
        from lrts.communication.ipc_message import IPCMessageType

        request: ProgressCreateRequest = ProgressCreateRequest(
            application_id=self._application_id,
            progress_id=progress_id,
            description=description,
            color=color,
            total=total,
            leave=leave,
            unit=unit
        )

        create_progress_data: CreateProgressIPCMessageData = CreateProgressIPCMessageData(
            create_info=request
        )

        create_progress_message: CreateProgressIPCMessage = CreateProgressIPCMessage(
            source_node_id=self._service_id,
            message_type=IPCMessageType.CREATE_PROGRESS,
            payload=create_progress_data
        )

        self._progress_ipc_pipe.send(create_progress_message)

        return progress_id

    def increment_progress(self, progress_id: str, amount: int) -> None:
        from lrts.communication.progress.progress_requests import ProgressIncrementRequest
        from lrts.communication.ipc_message import IncrementProgressIPCMessageData
        from lrts.communication.ipc_message import IncrementProgressIPCMessage
        from lrts.communication.ipc_message import IPCMessageType

        request: ProgressIncrementRequest = ProgressIncrementRequest(
            application_id=self._application_id,
            progress_id=progress_id,
            increment=amount
        )

        increment_data: IncrementProgressIPCMessageData = IncrementProgressIPCMessageData(
            increment_info=request
        )

        increment_message: IncrementProgressIPCMessage = IncrementProgressIPCMessage(
            source_node_id=self._service_id,
            message_type=IPCMessageType.INCREMENT_PROGRESS,
            payload=increment_data
        )

        self._progress_ipc_pipe.send(increment_message)

    def close_progress(self, progress_id: str) -> None:
        from lrts.communication.progress.progress_requests import ProgressCloseRequest
        from lrts.communication.ipc_message import CloseProgressIPCMessageData
        from lrts.communication.ipc_message import CloseProgressIPCMessage
        from lrts.communication.ipc_message import IPCMessageType

        request: ProgressCloseRequest = ProgressCloseRequest(
            application_id=self._application_id,
            progress_id=progress_id
        )

        close_data: CloseProgressIPCMessageData = CloseProgressIPCMessageData(
            close_info=request
        )

        close_message: CloseProgressIPCMessage = CloseProgressIPCMessage(
            source_node_id=self._service_id,
            message_type=IPCMessageType.CLOSE_PROGRESS,
            payload=close_data
        )

        self._progress_ipc_pipe.send(close_message)

    @property
    @abstractmethod
    def service_name(self) -> str:
        """Return the human-readable friendly name of the service."""

    @staticmethod
    @abstractmethod
    def run(service: Service) -> Any:
        """Run the service and return a pickle serializable result when finished."""

    @staticmethod
    def worker_begin_service(service_id: str, service: Service,
                             progress_ipc_pipe: Pipe, application_id: str) -> ServiceResult:
        service._progress_ipc_pipe = progress_ipc_pipe
        service._service_id = service_id
        service._application_id = application_id

        service_result: ServiceResult = ServiceResult(
            service_id=service_id,
            service_status=ServiceResultStatus.PENDING,
            service_result=None
        )

        try:
            service_result.service_result = service.run(service=service)
            service_result.service_status = ServiceResultStatus.FINISHED
        except Exception as e:
            # ToDo: Implement custom logger interface
            print(f'{service.service_name} CRASHED!!!')
            print(traceback.format_exc())
            print(e)

            service_result.service_status = ServiceResultStatus.CRASHED

        return service_result
