#!/usr/bin/env python3

import asyncio
import subprocess
import argparse

from datetime import datetime

from asyncio.exceptions import TimeoutError, CancelledError
from subprocess import TimeoutExpired


class Data:

    def __init__(self):
        self.__records = [
            {'id': 10, 'status': 'NEW', 'dc': 'DC-1'},
            {'id': 11, 'status': 'NEW', 'dc': 'DC-2'},
            {'id': 12, 'status': 'NEW', 'dc': 'DC-3'},
            {'id': 13, 'status': 'NEW', 'dc': 'DC-4'},
            {'id': 14, 'status': 'NEW', 'dc': 'DC-5'},
            {'id': 15, 'status': 'NEW', 'dc': 'DC-6'},
            {'id': 20, 'status': 'NEW', 'dc': 'DC-7'},
            {'id': 30, 'status': 'NEW', 'dc': 'DC-8'},
            {'id': 30, 'status': 'NEW', 'dc': 'DC-9'},
            {'id': 30, 'status': 'NEW', 'dc': 'DC-10'}
        ]
        self.__SSH_TIMEOUT = 30
        self.__DF_CMD = "/usr/bin/ssh -o StrictHostKeyChecking=no -p %port% root@%host% 'df -h /'"

    def get_records(self):
        return self.__records

    def process_sync(self, records):
        by_dcs = {}
        for record in records:
            dc = record["dc"]
            if record["dc"] not in by_dcs:
                by_dcs[dc] = []

            by_dcs[dc].append(record)

        for dc, data in by_dcs.items():
            self.__process_sync_cmd(dc, data, self.__DF_CMD)

    def __process_sync_cmd(self, dc, records, cmd):
        stdout = stderr = None
        print("Started task to process records of DC '{}'".format(dc))
        for record in records:
            print("Processing record with ID '{}' of DC {}".format(record["id"], record["dc"]))

            process = subprocess.Popen(
                cmd,
                shell=True,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            try:
                stdout, stderr = process.communicate(timeout=self.__SSH_TIMEOUT)
            except TimeoutExpired:
                print("Task of DC '{}' failed: Timeout".format(dc))

            if type(stdout) is bytes:
                stdout = stdout.decode()
            if type(stderr) is bytes:
                stderr = stderr.decode()

        if stderr:
            print("Task of DC '{}' failed with error:\n{}".format(dc, stdout))
        else:
            print("Task of DC '{}' completed:\n{}".format(dc, stdout))

    async def process_async(self, records):
        by_dcs = {}
        for record in records:
            dc = record["dc"]
            if record["dc"] not in by_dcs:
                by_dcs[dc] = []

            by_dcs[dc].append(record)

        tasks = []
        for dc, data in by_dcs.items():
            tasks.append({
                "name": dc,
                "ref": asyncio.create_task(
                    asyncio.wait_for(self.__process_async_cmd(dc, data, self.__DF_CMD), timeout=self.__SSH_TIMEOUT))
            })

        for task in tasks:
            try:
                await task["ref"]
            except TimeoutError:
                print("Task of DC '{}' failed: Timeout".format(task["name"]))
            except CancelledError:
                print("Task of DC '{}' failed: Cancelled".format(task["name"]))

    @staticmethod
    async def __process_async_cmd(dc, records, cmd):
        stdout = stderr = None
        print("Started task to process records of DC '{}'".format(dc))
        for record in records:
            print("Processing record with ID '{}' of DC {}".format(record["id"], record["dc"]))

            process = await asyncio.create_subprocess_shell(
                cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            if type(stdout) is bytes:
                stdout = stdout.decode()
            if type(stderr) is bytes:
                stderr = stderr.decode()

        if stderr:
            print("Task of DC '{}' failed with error:\n{}".format(dc, stdout))
        else:
            print("Task of DC '{}' completed:\n{}".format(dc, stdout))


async def main():
    HELP = "Please define run mode (sync|async)"
    argParser = argparse.ArgumentParser()
    argParser.add_argument("mode", metavar="mode", nargs="+", help=HELP)
    args = argParser.parse_args()
    if args.mode[0] not in ['sync', 'async']:
        print(HELP)
        exit(1)
    else:
        mode = args.mode[0]

    data = Data()
    records = data.get_records()

    start_timestamp = int(datetime.timestamp(datetime.now()))

    if mode == "sync":
        data.process_sync(records)
    else:
        await data.process_async(records)

    end_timestamp = int(datetime.timestamp(datetime.now()))
    print("--------------------------------------------------")
    print("Completed for {} seconds".format(end_timestamp - start_timestamp))


if __name__ == "__main__":
    asyncio.run(main())
