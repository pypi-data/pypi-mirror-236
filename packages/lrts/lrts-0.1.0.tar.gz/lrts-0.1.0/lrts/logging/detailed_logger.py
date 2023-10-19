import sys
from typing import Dict

import enlighten
from enlighten import Counter, StatusBar
from loguru import logger

from lrts.logging.log_level import LogLevel
from lrts.logging.logger import Logger


class DetailedLogger(Logger):
    def __init__(self, log_level: LogLevel, status_bar: bool, status_color: str,
                 initial_stage: str, min_delta: float) -> None:
        self.log_level = log_level
        self.status_bar = status_bar
        self.status_color = status_color
        self.initial_stage: str = initial_stage
        self.min_delta: float = min_delta

        self._counters: Dict[str, Counter] = {}

        self._status_manager = enlighten.get_manager()
        self._status_bar: StatusBar = self._status_manager.status_bar(status_format=u'lrts{fill}Stage: {stage}{fill}'
                                                                                    u'{elapsed}',
                                                                      color=status_color,
                                                                      justify=enlighten.Justify.CENTER,
                                                                      stage='Initializing Application',
                                                                      autorefresh=True, min_delta=0.5)

        logger.remove()
        logger.add(sys.stdout, format="[{time:HH:mm:ss}] <lvl>{message}</lvl>")

    def trace(self, msg: str) -> None:
        if self.log_level >= LogLevel.TRACE:
            logger.trace(msg)

    def debug(self, msg: str) -> None:
        if self.log_level >= LogLevel.DEBUG:
            logger.debug(msg)

    def info(self, msg: str) -> None:
        if self.log_level >= LogLevel.INFO:
            logger.info(msg)

    def success(self, msg: str) -> None:
        if self.log_level >= LogLevel.SUCCESS:
            logger.success(msg)

    def warning(self, msg: str) -> None:
        if self.log_level >= LogLevel.WARNING:
            logger.warning(msg)

    def error(self, msg: str) -> None:
        if self.log_level >= LogLevel.ERROR:
            logger.error(msg)

    def critical(self, msg: str) -> None:
        if self.log_level >= LogLevel.CRITICAL:
            logger.critical(msg)

    def set_stage(self, stage: str) -> None:
        self._status_bar.update(stage=stage)

    def create_counter(self, total: int, description: str, unit: str,
                       color: str, leave: bool, progress_id: str) -> None:
        if progress_id in self._counters:
            self.warning(f'create_counter: A counter with ID: {progress_id} already exists! You are resetting it!')

        counter: Counter = self._status_manager.counter(
            total=total,
            desc=description,
            unit=unit,
            color=color,
            leave=leave
        )
        self._counters[progress_id] = counter

    def update_counter(self, progress_id: str, amount: int = 1) -> None:
        if progress_id not in self._counters:
            self.warning(f'update_counter failed because no counter with ID: {progress_id} exists!')
            return

        counter: Counter = self._counters[progress_id]
        counter.update(incr=amount)

    def close_counter(self, progress_id: str) -> None:
        if progress_id not in self._counters:
            self.warning(f'close_counter failed because no counter with ID: {progress_id} exists!')
            return

        counter: Counter = self._counters[progress_id]
        counter.close()

        del self._counters[progress_id]

