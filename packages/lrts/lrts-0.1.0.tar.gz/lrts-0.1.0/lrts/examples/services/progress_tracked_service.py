from __future__ import annotations

import random
import time

from lrts.service import Service


class ProgressTrackedService(Service):
    def __init__(self, iterations_min: int = 25, iterations_max: int = 100,
                 sleep_seconds_min: int = 1, sleep_seconds_max: int = 2) -> None:
        super().__init__()

        self.iterations_min: int = iterations_min
        self.iterations_max: int = iterations_max
        self.sleep_seconds_min: int = sleep_seconds_min
        self.sleep_seconds_max: int = sleep_seconds_max

    def service_name(self) -> str:
        return "Progress Tracked Service Example"

    @staticmethod
    def run(service: ProgressTrackedService) -> None:
        total_iterations: int = random.randint(service.iterations_min, service.iterations_max)

        progress_id: str = service.create_progress(
            description='Doing Work',
            color='white',
            total=total_iterations,
            leave=True,
            unit='iterations'
        )

        for i in range(total_iterations):
            wait_time: int = random.randint(service.sleep_seconds_min, service.sleep_seconds_max)
            time.sleep(wait_time)

            service.increment_progress(progress_id=progress_id, amount=1)

        service.close_progress(progress_id=progress_id)
