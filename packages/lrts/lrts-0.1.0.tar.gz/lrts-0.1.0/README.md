# lrts (Long Running Task Service)

Distributed computation and task synchronization got you down? Look no further! `lrts` is designed to make distributing long running tasks and reporting on their progress over a networked cluster easier than ever!

`lrts` is a Python library meticulously crafted to streamline the execution of long running asynchronous network tasks. This tool fills the gap left by other distributed computing Python libraries that falter under the weight of extended tasks.

![lrts progress tracking showcase](lrts.gif)

## Overview

By subclassing the `Service` class, any code encapsulated within the `run` method is seamlessly scheduled for asynchronous remote execution. The root scheduler, acting as a beacon, delegates this code to an appropriate worker in the cluster.

### Highlights:

1. **Optimized for Longevity:** Unlike contemporary Python parallel libraries like Dask, `lrts` embraces long running tasks. Where others timeout or flash warnings, `lrts` thrives.
2. **Progress Reporting:** Inside the tightest loops, `lrts` provides lightweight, built-in progress reporting functionality. This ensures tasks justifying extended runtimes are tracked without a hitch.
3. **Communication Paradigm:** All task communication is adeptly managed by the main processes of the Application, Scheduler, and Worker tiers.
4. **Progress Sub-process:** Bypassing the limitations posed by Python's GIL, `lrts` spawns a unique sub-process for progress alone. This ensures uninterrupted and rapid progression of core tasks, even while reporting back on their advancement.
5. **Intelligent Latency Balancing:** The system intuitively captures the average latency for progress increments, optimizing network overhead by batching requests as per the observed latency.
6. **Resilient Task Management:** The library intelligently handles worker disconnects, reconnects, timeouts, and task rescheduling.
7. **Dynamic Cluster Adaptability:** Workers can be added and removed from the cluster at any time, even during ongoing tasks.
8. **Service Stability:** `lrts` ensures tasks resume or reschedule upon service crashes.
9. **Scheduler Independence:** Workers can commence tasks irrespective of the scheduler's state. The scheduler does not need to be online beforehand.

## Original Context

The genesis of `lrts` was in the financial sector — to efficiently process copious volumes of market data. For each market symbol and corresponding indicator + time scale, a distinct task would be relayed to the scheduler (Resulting in millions of long running tasks). These tasks were then distributed among worker machines, processed, and the results were compressed into a binary format. This compressed data would then find its way back to the application, reduced and refined, ready for subsequent layers of processing, ultimately feeding a NEAT-based AI model that also leverages lrts for population training.

`lrts` was specifically designed for AI training on financial data and was thus created with resilience in mind. Service/Worker crashes, machines out of memory, scheduler crashes, and many other issues are automatically handled allowing `lrts` to resume work.

The environment which `lrts` was designed for would often have scaling requirements from 0 workers to hundreds of thousands of workers, and was thus created to allow easy worker disconnect, connect, reconnect capabilities allowing clusters to dynamically scale to find a balance between cost and time.

## Why `lrts`?

1. **Tailored for Extended Tasks:** Existing libraries fall short with prolonged tasks, often clouding the visibility on task progress and ETA.
2. **Precision Progress Reporting:** Detailed and real-time progress feedback is crucial for long tasks, and `lrts` offers this without taxing the system.

## Usage
1. Install and run Scheduler/Worker/Progress Server
```commandline
# Install With Advanced Terminal Capabilities (Recommended)
pip install lrts[detailed_progress]

# Install Without Advanced Terminal Capabilities (For Those With Their Own Logging Solutions)
pip install lrts
```

Start The Scheduler:
```commandline
lrts scheduler -address 127.0.0.1 -port 5555 -timeout 1

Scheduler Command Line Options:
    address: The IP address on the machine to bind to
    port: The port to bind to
    timeout: The maximum time to spend decoding a single network packet (Almost always use 1 here unless you are transmitting large amounts of data in your services such as pickled files)
```

Start The Progress Server (If you need to track task progress):
```commandline
lrts progress-server -address 127.0.0.1 -port 5454 -timeout 1

Progress Server Command Line Options:
    address: The IP address on the machine to bind to
    port: The port to bind to
    timeout: The maximum time to spend decoding a single network packet (Almost always use 1 here unless you are transmitting large amounts of data in your services such as pickled files)
```

Start A Worker:
```commandline
lrts worker -scheduler-address 127.0.0.1 -scheduler-port 5555 -progress-address 127.0.0.1 -progress-port 5454 -max-jobs -1 -timeout 1

Worker Command Line Options:
    scheduler-address: The IP address of the scheduler server
    scheduler-port: The port of the scheduler server
    progress-address: The IP address of the progress server (If needed)
    progress-port: The port of the progress server (If needed)
    timeout: The maximum time to spend decoding a single network packet (Almost always use 1 here unless you are transmitting large amounts of data in your services such as pickled files)
    max-jobs: The maximum number of jobs to allow at once (Directly translating to subprocesses)
        if max-jobs = -1 Then system will use all physical cores
        if max-jobs = -2 Then system will use all logical cores
        if max-jobs = -3 Then system will use physical cores minus 1
        if max-jobs = -4 Then system will use logical cores minus 1
        
    In my experience using all avaialable cores tends to be slower then physical/logical cores minus 1
    This heavily depends on what you are using lrts for.
    You will notice significant performance changes when experimenting with this number. Especially between AWS/Google Cloud/Docker
    You should experiment here to find which brings the best performance for you.
```

2. Define a service. Note: Generally a service should be some piece of independent parallel code that justifies the network overhead of sending it to another machine, the example we use here for simplicity is not such a case.  Simply inherit from the `Service` class and encapsulate your desired code within the `run` method. From there, `lrts` will later take over, ensuring your code is executed on the optimal worker within the cluster.
```python
from __future__ import annotations
from typing import Union, Any

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
```

3. Run your code and synchronously wait for task completion
```python
from lrts import ApplicationInformation, ClientApplication, ServiceResult
from lrts.examples.services.mult_service import MultService

if __name__ == '__main__':
    application_information: ApplicationInformation = ApplicationInformation(
        scheduler_address='127.0.0.1',
        scheduler_port='5555',
        progress_server_address='127.0.0.1',
        progress_server_port='5454',
        progress_rtt_test_frequency=10_000,  # How often we check the round trip latency to the progress server
        communication_time_out=1,  # The amount of milliseconds to stall on receiving network data (1 is usually good)
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

    # Disconnect the application from the cluster so that it can discard remaining work and network queues if any
    # and free up memory for other applications
    application.stop_application()
```

4. Run multiple services on the cluster simultaneously and wait for their results synchronously
```python
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
        communication_time_out=1,  # The amount of milliseconds to stall on receiving network data (1 is usually good)
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

    # Disconnect the application from the cluster so that it can discard remaining work and network queues if any
    # and free up memory for other applications
    application.stop_application()
```
5. Run multiple services on the cluster simultaneously and perform some action as they are completed in no particular order
```python
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
    service_c: MultService = MultService(a=2, b=4)  # Create a third instance of the multiplication service

    # Non-Blocking
    service_id_a: str = application.schedule_service(service=service_a)  # Send the first service
    service_id_b: str = application.schedule_service(service=service_b)  # Send the second service
    service_id_c: str = application.schedule_service(service=service_c)  # Send the third service

    # Wait for the results in no particular order, but process them as they are completed
    service_ids: List[str] = [service_id_a, service_id_b, service_id_c]

    result: ServiceResult
    for result in application.as_completed(service_ids=service_ids):
        print(f'Service with ID: {result.service_id} finished with result: {result.service_result}')

    # Disconnect the application from the cluster so that it can discard remaining work and network queues if any
    # and free up memory for other applications
    application.stop_application()

```

## Future Improvements
1. Official documentation and usage webpage
2. Adding the ability to provide database credentials that allow serialized task results to be stored off of the scheduler/application/worker stack that are fetched only when the application needs them reducing memory overhead on application/scheduler/workers.
3. The library is extremely resilient to worker/scheduler disconnects & crashes but if the application that submitted the work disconnects or crashes workers will discard their results and the scheduler will remove all queued jobs and cancel running jobs. A major improvement would be to allow workers to finish their scheduled tasks serialize and save the results and have the scheduler continue running scheduled work while giving the application a very generous time frame to respond.

## Is this a Dask Replacement?
It depends on your use case. If you are currently using Dask to spawn long running processes on worker machines that work independently of eachother then yes, `lrts` can replace Dask and provide you with additional tools centered around independent paralell processing that dask does not have available.

If your tasks strongly depend on each other, or you are looking for mature integrations with various libraries such as numpy then Dask or a combination of `lrts` and Dask may be the correct choice.

## Final Thoughts

`lrts` isn't merely a library; it's an evolution in distributed computing for Python. It's designed for computational giants that demand more than just parallel execution — they need progress visibility, efficiency, reliability, and resilience.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

