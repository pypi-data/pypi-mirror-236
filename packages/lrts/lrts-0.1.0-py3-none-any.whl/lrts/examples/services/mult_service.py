from __future__ import annotations

import time
from typing import Union

from lrts.service import Service


class MultService(Service):
    def __init__(self, a: Union[int, float], b: Union[int, float]) -> None:
        super().__init__()

        self.a = a
        self.b = b

    def service_name(self) -> str:
        return "Multiplication Service Example"

    @staticmethod
    def run(service: MultService) -> Union[int, float]:
        return service.a * service.b
