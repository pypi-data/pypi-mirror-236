from dataclasses import dataclass, field


@dataclass
class ProgressIncrementRequest:
    application_id: str
    progress_id: str
    increment: int = field(default_factory=lambda: 1)


@dataclass
class ProgressCreateRequest:
    application_id: str
    progress_id: str
    description: str
    color: str
    total: int
    leave: bool
    unit: str


@dataclass
class ProgressCloseRequest:
    application_id: str
    progress_id: str
