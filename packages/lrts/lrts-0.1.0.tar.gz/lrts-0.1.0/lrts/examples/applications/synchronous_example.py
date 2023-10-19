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

    # Example of how to run a single service and synchronously wait for the result
    service: MultService = MultService(a=6, b=9)  # Create an instance of the example multiplication service
    service_id: str = application.schedule_service(service=service)  # Ask the scheduler to queue the work and get an ID
    result: ServiceResult = application.wait_for(service_id=service_id)  # Block the program and wait for the result

    print(f'Service with ID: {service_id} finished with result: {result.service_result}')  # Print the result

