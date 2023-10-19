import uuid
from dataclasses import field, dataclass


@dataclass
class ProgressClientInformation:
    server_address: str
    server_port: str
    progress_rtt_test_frequency: int = field(default_factory=lambda: 10_000)
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    communication_time_out: int = field(default_factory=lambda: 1)
