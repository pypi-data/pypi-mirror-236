from typing import List

from lrts import ApplicationInformation, ClientApplication, LogLevel, Logger, DetailedLogger, ServiceResult
from lrts.examples.services.progress_tracked_service import ProgressTrackedService

# REQUIRES ENLIGHTEN AND LOGURU TO RUN pip install using: 'pip install lrts[detailed_progress]'
if __name__ == '__main__':
    application_information: ApplicationInformation

    try:
        import enlighten
        from loguru import logger

        detailed_logger: Logger = DetailedLogger(
            log_level=LogLevel.TRACE,
            status_bar=True,
            status_color='bold_underline_bright_white_on_lightslategray',
            initial_stage='Initializing',
            min_delta=0.5
        )
        application_information: ApplicationInformation = ApplicationInformation(
            scheduler_address='127.0.0.1',
            scheduler_port='5555',
            progress_server_address='127.0.0.1',
            progress_server_port='5454',
            progress_rtt_test_frequency=10_000,
            communication_time_out=1,
            progress_iteration_timeout=2_000
        )
        client_application: ClientApplication = ClientApplication(
            application_information=application_information,
            logger=detailed_logger
        )
        client_application.start_application()

        # Example Of Multiple Tracked Services
        progress_service_a: ProgressTrackedService = ProgressTrackedService()
        progress_service_b: ProgressTrackedService = ProgressTrackedService()
        progress_service_c: ProgressTrackedService = ProgressTrackedService()

        progress_id_a: str = client_application.schedule_service(service=progress_service_a)
        progress_id_b: str = client_application.schedule_service(service=progress_service_b)
        progress_id_c: str = client_application.schedule_service(service=progress_service_c)

        detailed_logger.set_stage(stage='Waiting For Results')

        _: List[ServiceResult] = client_application.wait_for_multi(
            service_ids=[
                progress_id_a,
                progress_id_b,
                progress_id_c
            ]
        )

        client_application.stop_application()
    except ImportError:
        print("Cannot run this example without additional dependencies: [enlighten, loguru]")
        print("Please install lrts using the command: 'pip install lrts[detailed_progress] to correct this issue.'")
        print("Or install enlighten and loguru manually.")
