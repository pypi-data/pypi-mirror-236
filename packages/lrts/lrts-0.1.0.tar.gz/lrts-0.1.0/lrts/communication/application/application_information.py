import uuid
from dataclasses import dataclass, field


@dataclass
class ApplicationInformation:
    scheduler_address: str
    scheduler_port: str
    progress_server_address: str
    progress_server_port: str
    progress_rtt_test_frequency: int = field(default_factory=lambda: 10_000)
    progress_iteration_timeout: int = field(default_factory=lambda: 2_000)
    communication_time_out: int = field(default_factory=lambda: 1)
    application_id: str = field(default_factory=lambda: str(uuid.uuid4()))
