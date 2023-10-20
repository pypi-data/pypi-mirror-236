import math
import time
import os
import random
import sys

work_break_default = 60 * 10  # Set to 15 for "infinite"
randomize_work_break_default = 'False'
cpu_intensity_default = 1
deplete_after_default = 2
max_primes_default = 25
memory_mb_default = 1

def is_prime(number):
    for x in range(2, int(math.sqrt(number) + 1)):
        if number % x == 0:
            return False
    return True

def compute_primes(cpu_intensity, start_at=1e15, max_primes=25):
    prime_count = 0
    number = start_at if start_at % 2 == 1 else start_at - 1
    while prime_count < max_primes:
        if is_prime(number):
            prime_count += 1
        number += 2
        # Sleep before starting next round.  Higher->lower CPU load.
        # cpu_intensity; helps control cpu utilization
        time.sleep(cpu_intensity)

def consume_memory(mem_mb):
    return bytearray(round(mem_mb*1024*1024))

def get_cpu_load(cpu_intensity):
    if cpu_intensity <=.2:
        return 'high'
    elif .2 < cpu_intensity < .85:
        return 'moderate'
    else:
        return 'low'

def triggered_w_load(cpu_intensity=0, max_primes=1, memory_mb=1):
    # Set random cpu_intensity if passed 0
    if cpu_intensity == 0:
        cpu_intensity = round(random.uniform(0.01, 1), 2)
    
    print(
        f"Starting triggered workload.  CPU Intensity: {cpu_intensity} ({get_cpu_load(cpu_intensity)}), max_primes: {max_primes}, memory_mb: {memory_mb}\n")
    start = time.time()

    # Set memory load
    memory_holder = consume_memory(memory_mb)

    # Begin CPU load
    compute_primes(cpu_intensity=cpu_intensity,
                   start_at=1e13, max_primes=max_primes)
    end = time.time()
    print(
        f"Completed triggered workload.  CPU Intensity: {cpu_intensity} ({get_cpu_load(cpu_intensity)}), max_primes: {max_primes}. Workload took {end-start} seconds, using {round(sys.getsizeof(memory_holder)/1024/1024,2)}MB Memory\n")
    return f"Done. Completed in {end-start}s\n"


def triggered_no_load(sleep_time=1):
    print(f"Starting triggered no-load process.  Sleep time: {sleep_time}\n")
    start = time.time()
    time.sleep(sleep_time)
    end = time.time()
    print(
        f"Completed triggered no-load process.  Sleep time: {sleep_time}.  Completed in {end-start} seconds.\n")
    return f"Done. Completed in {end-start}s\n"


class LoadGen:
    """Class for encapsulating a persistant "do work" process."""

    def __init__(self, work_break, cpu_intensity, deplete_after, max_primes, randomize_work_break=False, memory_mb=1):
        """Constructor.

        ARGS
          work_break (float): # seconds we want to wait before starting another
            round of work. Is the distinction between finite and infinite workloads.
          cpu_intensity (float):  # seconds we wait to do another load of work. How
            often we want to utilize cpu. Can be used to fine-tune cpu utilization
            between rounds of work.
          deplete_after (int): Number of loads of work done between rounds.
        """
        self.work_break = work_break
        self.randomize_work_break = randomize_work_break
        self.cpu_intensity = cpu_intensity
        self.deplete_after = deplete_after
        self.max_primes = max_primes
        self.memory_mb = memory_mb

    def start_workloads(self):
        """Workload(s) starter."""
        num_workloads = 0

        while True:
            num_workloads += 1
            # Set memory load
            memory_holder = consume_memory(self.memory_mb)
            
            # do a lot of work
            start = time.time()
            compute_primes(self.cpu_intensity)
            end = time.time()
            print(f"Workload took {end-start} seconds, using {round(sys.getsizeof(memory_holder)/1024/1024,2)}MB Memory\n")

            # check if we've done enough work loads to break out
            if num_workloads >= self.deplete_after:
                break

    def run(self):
        """Starts Infinite Workloads Loop."""

        while True:
            if self.randomize_work_break:
                self.work_break = random.randint(15, self.work_break)
            
            # Set random cpu_intensity if passed 0
            if self.cpu_intensity == 0:
                self.cpu_intensity = round(random.uniform(0.01, 1), 2)


            print(
                f"Starting a work loop: work: {self.work_break} (Random: {self.randomize_work_break}), CPU Intensity: {self.cpu_intensity} ({get_cpu_load(self.cpu_intensity)}), max_primes: {self.max_primes}, memory_mb: {self.memory_mb}\n")
            self.start_workloads()
            print(
                f"Waiting for {self.work_break} seconds before starting next work loop\n"
            )
            time.sleep(self.work_break)


def constant_loadgen(**kwargs):
    if os.environ.get("LOADGEN_RANDOMIZE_WORK_BREAK", randomize_work_break_default) == 'True':
        randomize_work_break = True
    else:
        randomize_work_break = False

    work_break = int(os.environ.get(
        "LOADGEN_WORK_BREAK", kwargs.setdefault('work_break', work_break_default)))
    cpu_intensity = float(os.environ.get(
        "LOADGEN_CPU_INTENSITY", kwargs.setdefault('cpu_intensity', cpu_intensity_default)))
    deplete_after = int(os.environ.get(
        "LOADGEN_DEPLETE_AFTER", kwargs.setdefault('deplete_after', deplete_after_default)))
    max_primes = int(os.environ.get(
        "LOADGEN_MAX_PRIMES", kwargs.setdefault('max_primes', max_primes_default)))
    memory_mb = float(os.environ.get(
        "LOADGEN_MEMORY_MB", kwargs.setdefault('memory_mb', memory_mb_default)))
        
    loadgen_worker = LoadGen(work_break=work_break, randomize_work_break=randomize_work_break,
                             cpu_intensity=cpu_intensity, deplete_after=deplete_after, max_primes=max_primes, memory_mb=memory_mb)
    return loadgen_worker
