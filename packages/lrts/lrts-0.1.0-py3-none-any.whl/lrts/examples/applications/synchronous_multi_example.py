from typing import List

from lrts import ApplicationInformation, ClientApplication, ServiceResult
from lrts.examples.services.mult_service import MultService

if __name__ == '__main__':
    application_information: ApplicationInformation = ApplicationInformation(
        scheduler_address='127.0.0.1',
        scheduler_port='5555',
        progress_server_address='127.0.0.1',
        progress_server_port='5454',
        progress_rtt_test_frequency=10_000,  # How often we check the round trip latency to the progress server
        communication_time_out=1,  # The amount of seconds to stall on receiving network data (1 is usually good)
        progress_iteration_timeout=2_000  # The max time to spend on status updates before resuming work
    )

    # The main resource for sending and receiving results to/from the cluster.
    application: ClientApplication = ClientApplication(
        application_information=application_information
    )

    # Tell the application to start its subprocesses and connect to the scheduler
    # The scheduler does not actually have to be running yet, the application will wait for it to be available.
    # Note that start_application will not block if the scheduler is not available.
    application.start_application()

    # Example of how to execute multiple services over the network in parallel and wait synchronously for the results
    service_a: MultService = MultService(a=6, b=9)  # Create an instance of the example multiplication service
    service_b: MultService = MultService(a=1, b=0)  # Create a separate instance of the multiplication service

    # Non-Blocking
    service_id_a: str = application.schedule_service(service=service_a)  # Send the first service
    service_id_b: str = application.schedule_service(service=service_b)  # Send the second service

    # Wait for the results in no particular order. Will return only once all results are ready.
    # See later example to get results as they are completed
    results: List[ServiceResult] = application.wait_for_multi(
        service_ids=[service_id_a, service_id_b]
    )

    result: ServiceResult
    for result in results:
        print(f'Service with ID: {result.service_id} finished with result: {result.service_result}')
