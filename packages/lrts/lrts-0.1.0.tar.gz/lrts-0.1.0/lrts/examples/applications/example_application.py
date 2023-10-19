from typing import List

from lrts.communication.application.application import Application
from lrts.communication.application.application_information import ApplicationInformation
from lrts.examples.services.mult_service import MultService
from lrts.examples.services.progress_tracked_service import ProgressTrackedService
from lrts.service import ServiceResult

if __name__ == '__main__':
    from lrts.communication.application.zmq_application import ZMQApplication

    application_information: ApplicationInformation = ApplicationInformation(
        scheduler_address='127.0.0.1',
        scheduler_port='5555',
        progress_server_address='127.0.0.1',
        progress_server_port='5454',
        progress_rtt_test_frequency=10_000,
        communication_time_out=1,
        progress_iteration_timeout=2_000
    )
    application: Application = ZMQApplication(
        application_information=application_information
    )
    application.start_application()

    # Example of how to run a single service and wait for the result
    service: MultService = MultService(a=10, b=5)
    service_id: str = application.schedule_service(service=service)
    result: ServiceResult = application.wait_for(service_id=service_id)

    print(f'Service with ID: {service_id} finished with result: {result.service_result}')

    # Example of how to run multiple services and wait for their results to complete
    service_a: MultService = MultService(a=1, b=1)
    service_b: MultService = MultService(a=2, b=2)
    service_c: MultService = MultService(a=3, b=3)

    id_a: str = application.schedule_service(service=service_a)
    id_b: str = application.schedule_service(service=service_b)
    id_c: str = application.schedule_service(service=service_c)

    results: List[ServiceResult] = application.wait_for_multi(
        service_ids=[
            id_a, id_b, id_c
        ]
    )

    result: ServiceResult
    for result in results:
        print(f'Service with ID [{result.service_id}] finished with result: {result.service_result}')

    # Example of progressed tracked services
    progress_service_a: ProgressTrackedService = ProgressTrackedService()
    progress_service_b: ProgressTrackedService = ProgressTrackedService()
    progress_service_c: ProgressTrackedService = ProgressTrackedService()

    progress_id_a: str = application.schedule_service(service=progress_service_a)
    progress_id_b: str = application.schedule_service(service=progress_service_b)
    progress_id_c: str = application.schedule_service(service=progress_service_c)

    _: List[ServiceResult] = application.wait_for_multi(
        service_ids=[
            progress_id_a, progress_id_b, progress_id_c
        ]
    )

    application.stop_application()
