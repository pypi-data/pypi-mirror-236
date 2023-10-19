import uuid
from dataclasses import field, dataclass


@dataclass
class WorkerInformation:
    scheduler_address: str
    scheduler_port: str
    progress_server_address: str
    progress_server_port: str
    max_simultaneous_jobs: int
    progress_rtt_test_frequency: int = field(default_factory=lambda: 10_000)
    communication_time_out: int = field(default_factory=lambda: 1)
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
