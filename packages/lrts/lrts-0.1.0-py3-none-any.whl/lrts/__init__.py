from typing import TypeAlias

from lrts.communication.application.application_information import ApplicationInformation
from lrts.communication.application.zmq_application import ZMQApplication
from lrts.logging.log_level import LogLevel
from lrts.logging.logger import Logger
from lrts.logging.detailed_logger import DetailedLogger
from lrts.service import ServiceResult


ClientApplication: TypeAlias = ZMQApplication
