import datetime
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum


class NodeType(Enum):
    SCHEDULER = "SCHEDULER"
    APPLICATION = "APPLICATION"
    WORKER = "WORKER"


@dataclass
class Node:
    node_type: NodeType
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: float = field(default_factory=lambda: time.time())

@dataclass
class SchedulerNode(Node):
    node_type: NodeType = NodeType.SCHEDULER


@dataclass
class ApplicationNode(Node):
    node_type: NodeType = NodeType.APPLICATION


@dataclass
class WorkerNode(Node):
    node_type: NodeType = NodeType.WORKER
