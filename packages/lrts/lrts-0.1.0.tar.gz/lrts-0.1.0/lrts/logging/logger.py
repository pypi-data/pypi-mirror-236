from abc import abstractmethod

from lrts.logging.log_level import LogLevel
from lrts.types.singleton import SingletonABCMeta


class Logger(metaclass=SingletonABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def trace(self, msg: str) -> None:
        """Log a trace message if the current log_level permits it."""

    @abstractmethod
    def debug(self, msg: str) -> None:
        """Log a debug message if the current log_level permits it."""

    @abstractmethod
    def info(self, msg: str) -> None:
        """Log an info message if the current log_level permits it."""

    @abstractmethod
    def success(self, msg: str) -> None:
        """Log a success message if the current log_level permits it."""

    @abstractmethod
    def warning(self, msg: str) -> None:
        """Log a warning message if the current log_level permits it."""

    @abstractmethod
    def error(self, msg: str) -> None:
        """Log an error message if the current log_level permits it."""

    @abstractmethod
    def critical(self, msg: str) -> None:
        """Log a critical message if the current log_level permits it."""

    @abstractmethod
    def set_stage(self, stage: str) -> None:
        """Update the status bar stage if the logger supports it otherwise pass."""

    @abstractmethod
    def create_counter(self, total: int, description: str, unit: str,
                       color: str, leave: bool, progress_id: str) -> None:
        """Create and start tracking a progress bar if the logger supports it otherwise pass."""

    @abstractmethod
    def update_counter(self, progress_id: str, amount: int = 1) -> None:
        """Increment the requested progress bar."""

    @abstractmethod
    def close_counter(self, progress_id: str) -> None:
        """Close the requested progress bar."""
