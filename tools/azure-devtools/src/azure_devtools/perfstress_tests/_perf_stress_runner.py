# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import argparse
import asyncio
import time
import inspect
import logging
import os
import pkgutil
import sys
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from ._perf_stress_base import _PerfTestABC
from ._batch_perf_test import BatchPerfTest
from ._perf_stress_test import PerfStressTest
from ._repeated_timer import RepeatedTimer


class _PerfStressRunner:
    def __init__(self, test_folder_path: Optional[str] = None, debug: bool = False):
        self._tests: List[_PerfTestABC] = []
        self._operation_status_tracker: int = -1

        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        if debug:
            self.logger.setLevel(level=logging.DEBUG)
            handler.setLevel(level=logging.DEBUG)
        else:
            self.logger.setLevel(level=logging.INFO)
            handler.setLevel(level=logging.INFO)
        self.logger.addHandler(handler)

        # NOTE: If you need to support registering multiple test locations, move this into Initialize, call lazily on Run, expose RegisterTestLocation function.
        self._discover_tests(test_folder_path or os.getcwd())
        self._parse_args()

    def _get_completed_operations(self) -> int:
        return sum([t.completed_operations for t in self._tests])

    def _get_operations_per_second(self) -> float:
        test_results = [(t.completed_operations, t.last_completion_time) for t in self._tests]
        return sum(map(lambda x: x[0] / x[1] if x[1] else 0, test_results))

    def _parse_args(self):
        # First, detect which test we're running.
        arg_parser = argparse.ArgumentParser(
            description="Python Perf Test Runner", usage="{} <TEST> [<args>]".format(__file__)
        )

        # NOTE: remove this and add another help string to query for available tests
        # if/when # of classes become enough that this isn't practical.
        arg_parser.add_argument(
            "test", help="Which test to run.  Supported tests: {}".format(" ".join(sorted(self._test_classes.keys())))
        )

        args = arg_parser.parse_args(sys.argv[1:2])
        try:
            self._test_class_to_run = self._test_classes[args.test]
        except KeyError as e:
            self.logger.error(
                "Invalid test: {}\n    Test must be one of: {}\n".format(
                    args.test, " ".join(sorted(self._test_classes.keys()))
                )
            )
            raise

        # Next, parse args for that test.  We also do global args here too so as not to confuse the initial test parse.
        per_test_arg_parser = argparse.ArgumentParser(
            description=self._test_class_to_run.__doc__ or args.test, usage="{} {} [<args>]".format(__file__, args.test)
        )

        # Global args
        per_test_arg_parser.add_argument(
            "-p", "--parallel", nargs="?", type=int, help="Degree of parallelism to run with.  Default is 1.", default=1
        )
        per_test_arg_parser.add_argument(
            "-d", "--duration", nargs="?", type=int, help="Duration of the test in seconds.  Default is 10.", default=10
        )
        per_test_arg_parser.add_argument(
            "-i",
            "--iterations",
            nargs="?",
            type=int,
            help="Number of iterations in the main test loop.  Default is 1.",
            default=1,
        )
        per_test_arg_parser.add_argument(
            "-w", "--warmup", nargs="?", type=int, help="Duration of warmup in seconds.  Default is 5.", default=5
        )
        per_test_arg_parser.add_argument(
            "--no-cleanup", action="store_true", help="Do not run cleanup logic.  Default is false.", default=False
        )
        per_test_arg_parser.add_argument(
            "--sync", action="store_true", help="Run tests in sync mode.  Default is False.", default=False
        )
        per_test_arg_parser.add_argument(
            "--profile", action="store_true", help="Run tests with profiler.  Default is False.", default=False
        )
        per_test_arg_parser.add_argument(
            "-x", "--test-proxies", help="URIs of TestProxy Servers (separated by ';')",
            type=lambda s: s.split(';')
        )
        per_test_arg_parser.add_argument(
            "--insecure", action="store_true", help="Disable SSL validation. Default is False.", default=False
        )

        # Per-test args
        self._test_class_to_run.add_arguments(per_test_arg_parser)
        self.per_test_args = per_test_arg_parser.parse_args(sys.argv[2:])

        self.logger.info("")
        self.logger.info("=== Options ===")
        self.logger.info(args)
        self.logger.info(self.per_test_args)
        self.logger.info("")

    def _discover_tests(self, test_folder_path):
        self._test_classes = {}
        if os.path.isdir(os.path.join(test_folder_path, 'tests')):
            test_folder_path = os.path.join(test_folder_path, 'tests')
        self.logger.debug("Searching for tests in {}".format(test_folder_path))

        # Dynamically enumerate all python modules under the tests path for classes that implement PerfStressTest
        for loader, name, _ in pkgutil.walk_packages([test_folder_path]):
            try:
                module = loader.find_module(name).load_module(name)
            except Exception as e:
                self.logger.debug("Unable to load module {}: {}".format(name, e))
                continue
            for name, value in inspect.getmembers(module):
                if name.startswith("_"):
                    continue
                if inspect.isclass(value):
                    if issubclass(value, _PerfTestABC) and value not in [PerfStressTest, BatchPerfTest]:
                        self.logger.info("Loaded test class: {}".format(name))
                        self._test_classes[name] = value

    async def start(self):
        self.logger.info("=== Setup ===")
        self._tests = [self._test_class_to_run(self.per_test_args) for _ in range(self.per_test_args.parallel)]

        try:
            try:
                await self._tests[0].global_setup()
                try:
                    await asyncio.gather(*[test.setup() for test in self._tests])
                    self.logger.info("")
                    self.logger.info("=== Post Setup ===")
                    await asyncio.gather(*[test.post_setup() for test in self._tests])
                    self.logger.info("")

                    if self.per_test_args.warmup and not self.per_test_args.profile:
                        await self._run_tests("Warmup", self.per_test_args.warmup)

                    for i in range(self.per_test_args.iterations):
                        title = "Test" if self.per_test_args.iterations == 1 else "Test {}".format(i + 1)
                        await self._run_tests(title, self.per_test_args.duration)
                except Exception as e:
                    self.logger.warn("Exception: " + str(e))
                finally:
                    self.logger.info("=== Pre Cleanup ===")
                    await asyncio.gather(*[test.pre_cleanup() for test in self._tests])
                    self.logger.info("")

                    if not self.per_test_args.no_cleanup:
                        self.logger.info("=== Cleanup ===")
                        await asyncio.gather(*[test.cleanup() for test in self._tests])
            except Exception as e:
                self.logger.warn("Exception: " + str(e))
            finally:
                if not self.per_test_args.no_cleanup:
                    await self._tests[0].global_cleanup()
        except Exception as e:
            self.logger.warn("Exception: " + str(e))
        finally:
            await asyncio.gather(*[test.close() for test in self._tests])

    async def _run_tests(self, title: str, duration: int) -> None:
        self._operation_status_tracker = -1
        status_thread = RepeatedTimer(1, self._print_status, title)
        try:
            if self.per_test_args.sync:
                with ThreadPoolExecutor(max_workers=self.per_test_args.parallel) as ex:
                    futures = [ex.submit(test.run_all_sync, duration) for test in self._tests]
                    for future in as_completed(futures):
                        future.result()
                    
            else:
                tasks = [test.run_all_async(duration) for test in self._tests]
                await asyncio.gather(*tasks)
        finally:
            status_thread.stop()

        self.logger.info("")
        self.logger.info("=== Results ===")

        total_operations = self._get_completed_operations()
        operations_per_second = self._get_operations_per_second()
        if operations_per_second:
            seconds_per_operation = 1 / operations_per_second
            weighted_average_seconds = total_operations / operations_per_second
            self.logger.info(
                "Completed {:,} operations in a weighted-average of {:,.2f}s ({:,.2f} ops/s, {:,.3f} s/op)".format(
                    total_operations, weighted_average_seconds, operations_per_second, seconds_per_operation
                )
            )
        else:
            self.logger.info("Completed without generating operation statistics.")
        self.logger.info("")

    def _print_status(self, title):
        if self._operation_status_tracker == -1:
            self._operation_status_tracker = 0
            self.logger.info("=== {} ===\nCurrent\t\tTotal\t\tAverage".format(title))

        total_operations = self._get_completed_operations()
        current_operations = total_operations - self._operation_status_tracker
        average_operations = self._get_operations_per_second()

        self._operation_status_tracker = total_operations
        self.logger.info("{}\t\t{}\t\t{:.2f}".format(current_operations, total_operations, average_operations))
