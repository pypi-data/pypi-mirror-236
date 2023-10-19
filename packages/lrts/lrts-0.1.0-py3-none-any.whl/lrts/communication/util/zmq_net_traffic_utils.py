import pickle
from typing import List, Any, Union

from lrts.communication.ipc_message import IPCMessage


def zmq_net_traffic_to_ipc_messages(traffic: List[Any]) -> Union[List[IPCMessage], None]:
    messages: List[IPCMessage] = []

    if len(traffic) != 2:
        print(f'Received Invalid Network Traffic 1: {traffic}')  # ToDo: Implement custom logger interface
        return None

    source_id, payload_encoded = traffic

    try:
        _ = source_id.decode('utf-8')
    except UnicodeDecodeError:
        print(f'Received Invalid Network Traffic: {traffic}')   # ToDo: Implement custom logger interface
        return None

    try:
        ipc_payload = pickle.loads(payload_encoded)
        if not isinstance(ipc_payload, IPCMessage):
            print(f'Received Invalid Network Traffic: {traffic}')   # ToDo: Implement custom logger interface
            return None
    except (pickle.UnpicklingError, AttributeError, EOFError, ImportError, IndexError):
        print(f'Received Invalid Network Traffic: {traffic}')   # ToDo: Implement custom logger interface
        return None

    messages.append(ipc_payload)

    return messages if messages else None
