from dataclasses import dataclass, field
from typing import Dict

from lrts.logging.log_level import LogLevel
from lrts.logging.logger import Logger


@dataclass
class PrintLoggerCounter:
    total: int
    description: str
    unit: str
    color: str
    leave: bool
    progress_id: str
    current: int = field(default_factory=lambda: 0)


class PrintLogger(Logger):
    def __init__(self, log_level: LogLevel, status_bar: bool, status_color: str,
                 initial_stage: str, min_delta: float) -> None:
        self.log_level = log_level
        self.status_bar = status_bar
        self.status_color = status_color
        self.initial_stage: str = initial_stage
        self.min_delta: float = min_delta

        self._counters: Dict[str, PrintLoggerCounter] = {}

    def trace(self, msg: str) -> None:
        if self.log_level >= LogLevel.TRACE:
            print(msg)

    def debug(self, msg: str) -> None:
        if self.log_level >= LogLevel.DEBUG:
            print(msg)

    def info(self, msg: str) -> None:
        if self.log_level >= LogLevel.INFO:
            print(msg)

    def success(self, msg: str) -> None:
        if self.log_level >= LogLevel.SUCCESS:
            print(msg)

    def warning(self, msg: str) -> None:
        if self.log_level >= LogLevel.WARNING:
            print(msg)

    def error(self, msg: str) -> None:
        if self.log_level >= LogLevel.ERROR:
            print(msg)

    def critical(self, msg: str) -> None:
        if self.log_level >= LogLevel.CRITICAL:
            print(msg)

    def set_stage(self, stage: str) -> None:
        pass

    def create_counter(self, total: int, description: str, unit: str,
                       color: str, leave: bool, progress_id: str) -> None:
        self.trace(msg="CREATE")
        new_counter: PrintLoggerCounter = PrintLoggerCounter(
            total=total,
            description=description,
            unit=unit,
            color=color,
            leave=leave,
            progress_id=progress_id
        )

        if progress_id in self._counters:
            self.warning(msg=f'A counter with ID: {progress_id} already exists. You are overwriting and resetting it!')

        self._counters[progress_id] = new_counter

    def update_counter(self, progress_id: str, amount: int = 1) -> None:
        if progress_id not in self._counters:
            self.warning(f'update_counter failed because no counter with ID: {progress_id} exists!')
            return

        self._counters[progress_id].current += amount

        total: int = self._counters[progress_id].total
        current: int = self._counters[progress_id].current

        self.trace(f'{current}/{total}')

    def close_counter(self, progress_id: str) -> None:
        self.trace(msg="CLOSE")
        if progress_id not in self._counters:
            self.warning(f'close_counter failed because no counter with ID: {progress_id} exists!')
            return

        del self._counters[progress_id]
