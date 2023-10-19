import argparse
import multiprocessing
import os
import platform


def main():
    parser = argparse.ArgumentParser(description="LRts Distributed Task Service CLI")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-command help")

    # Scheduler Command
    parser_scheduler = subparsers.add_parser("scheduler", help="Run the scheduler")
    parser_scheduler.add_argument("-address", type=str, required=True, help="The address to bind to")
    parser_scheduler.add_argument("-port", type=str, required=True, help="The port to bind to")
    parser_scheduler.add_argument("-timeout", type=int, required=True, help="Scheduler Timeout")

    # Worker Command
    parser_worker = subparsers.add_parser("worker", help="Run the worker")
    parser_worker.add_argument("-scheduler-address", type=str, required=True, help="IP address of the scheduler")
    parser_worker.add_argument("-scheduler-port", type=str, required=True, help="Port of the scheduler")
    parser_worker.add_argument("-progress-address", type=str, required=True, help="The IP address of the progress server")
    parser_worker.add_argument("-progress-port", type=str, required=True, help="The port of the progress server")
    parser_worker.add_argument("-max-jobs", type=int, required=True, help="Max tasks to accept simultaneously. -1 to use all physical cores. -2 to use all logical cores. -3 to use physical cores minus 1. -4 to use logical cores minus 1")
    parser_worker.add_argument("-timeout", type=int, required=True, help="Worker Timeout")

    # Progress Server Command
    parser_progress_server = subparsers.add_parser("progress-server", help="Run the progress server")
    parser_progress_server.add_argument("-address", type=str, required=True, help="The address to bind to")
    parser_progress_server.add_argument("-port", type=str, required=True, help="The port to bind to")
    parser_progress_server.add_argument("-timeout", type=int, required=True, help="Server Timeout")

    args = parser.parse_args()
    handle_command(args)


def get_physical_cores_linux():
    command = "lscpu -p | egrep -v '^#' | sort -u -t, -k 2,4 | wc -l"
    try:
        return int(os.popen(command).read())
    except:
        return None

def get_physical_cores_windows():
    command = "wmic cpu get NumberOfCores"
    try:
        return int(os.popen(command).read().split()[-1])
    except:
        return None

def get_physical_cores_mac():
    command = "sysctl -n hw.physicalcpu"
    try:
        return int(os.popen(command).read())
    except:
        return None

def get_logical_cores():
    return multiprocessing.cpu_count()


def handle_command(args):
    if args.command == "scheduler":
        handle_scheduler_command(args)

    if args.command == "worker":
        handle_worker_command(args)

    if args.command == "progress-server":
        handle_progress_server_command(args)


def handle_scheduler_command(args):
    from lrts.communication.router.zmq_scheduler_router import ZMQSchedulerRouter
    from lrts.communication.scheduler.zmq_scheduler import ZMQScheduler
    from lrts.communication.router.scheduler_router import SchedulerRouter
    from lrts.communication.scheduler.scheduler import Scheduler

    scheduler_router: SchedulerRouter = ZMQSchedulerRouter(
        bind_address=args.address,
        bind_port=args.port,
        communication_time_out=args.timeout
    )

    scheduler: Scheduler = ZMQScheduler(router=scheduler_router)

    try:
        scheduler.start_scheduler()

        while True:
            pass
    except KeyboardInterrupt:
        print("Cleaning up scheduler resources...")
    finally:
        scheduler.stop_scheduler()


def handle_worker_command(args):
    from lrts.communication.worker.worker_information import WorkerInformation
    from lrts.communication.router.worker_router import WorkerRouter
    from lrts.communication.router.zmq_worker_router import ZMQWorkerRouter
    from lrts.communication.worker.zmq_worker import ZMQWorker
    from lrts.communication.worker.worker import Worker

    logical_core_count: int = multiprocessing.cpu_count()
    physical_core_count: int = -1

    system: str = platform.system()

    match system:
        case "Linux":
            physical_core_count = get_physical_cores_linux()
        case "Windows":
            physical_core_count = get_physical_cores_windows()
        case "Darwin":
            physical_core_count = get_physical_cores_mac()
        case _:
            physical_core_count = -1

    if physical_core_count == -1:
        physical_core_count = logical_core_count
        print("Failed to determine physical core count. Falling back to logical core count.")

    target_cpu_count: int = 0

    match args.max_jobs:
        case -1:
            target_cpu_count = physical_core_count
        case -2:
            target_cpu_count = logical_core_count
        case -3:
            target_cpu_count = physical_core_count - 1
        case -4:
            target_cpu_count = logical_core_count - 1
        case _:
            target_cpu_count = args.max_jobs

    worker_information: WorkerInformation = WorkerInformation(
        scheduler_address=args.scheduler_address,
        scheduler_port=args.scheduler_port,
        progress_server_address=args.progress_address,
        progress_server_port=args.progress_port,
        max_simultaneous_jobs=target_cpu_count,
        communication_time_out=args.timeout
    )

    worker_router: WorkerRouter = ZMQWorkerRouter(worker_information=worker_information)

    worker: Worker = ZMQWorker(worker_information=worker_information, router=worker_router)

    try:
        worker.start_worker()

        while True:
            pass
    except KeyboardInterrupt:
        print("Cleaning Up Worker Resources...")
    finally:
        worker.stop_worker()


def handle_progress_server_command(args):
    from lrts.communication.router.progress_server_router import ProgressServerRouter
    from lrts.communication.router.zmq_progress_server_router import ZMQProgressServerRouter
    from lrts.communication.progress.progress_server import ProgressServer
    from lrts.communication.progress.zmq_progress_server import ZMQProgressServer

    progress_router: ProgressServerRouter = ZMQProgressServerRouter(
        bind_address=args.address,
        bind_port=args.port,
        communication_time_out=args.timeout
    )

    progress_server: ProgressServer = ZMQProgressServer(router=progress_router)

    try:
        progress_server.start_server()

        while True:
            pass
    except KeyboardInterrupt:
        print("Cleaning up server resources...")
    finally:
        progress_server.stop_server()
