"""Generate random instances, measure CPU runtimes, and print results.

Run: python runtime_testing.py
Both Gale-Shapley and brute force run on the same sizes and random instances.
Brute force has no timeout and may take impractically long at larger sizes.

Each instance has two groups of n people with complete random preferences.
Generation and printing are excluded from timing. Fast instances are repeated
and total CPU time is divided by the number of runs.
Only one instance is held at a time.
"""

import gc
import random
from time import process_time_ns

from gale_shapley import gale_shapley
from groups import Person, group

GROUP_SIZES_A = (2, 5, 10, 25, 50, 100, 500)
GROUP_SIZES_B = (2, 3, 5, 8, 10)
INSTANCES_PER_SIZE = 10
SEED = 422
MIN_CPU_SECONDS = 0.1


def generate_instance(size, seed):
    """Generate both groups reproducibly from the printed seed."""
    rng = random.Random(seed)

    def make_group():
        return group(size, [
            Person(person_id, rng.sample(range(size), size))
            for person_id in range(size)
        ])

    return make_group(), make_group()


def benchmark(algorithm_name, algorithm, sizes, *, instances=INSTANCES_PER_SIZE,
              seed=SEED):
    """Print each instance's CPU seconds and each size's mean."""
    print(f"\n{algorithm_name}", flush=True)
    average_times = {}
    for size in sizes:
        runtimes = []
        for trial in range(1, instances + 1):
            # Shared sizes/trials use the same preferences across algorithms.
            instance_seed = f"{seed}:{size}:{trial}"
            print(f"n={size}, instance={trial}/{instances}, seed={instance_seed}", flush=True)
            first, second = generate_instance(size, instance_seed)
            gc.collect()
            start = process_time_ns()
            runs = 0
            total_cpu_seconds = 0
            # Slow instances run once; fast ones repeat on the same preferences.
            while total_cpu_seconds < MIN_CPU_SECONDS:
                matching = algorithm(first, second)
                runs += 1
                total_cpu_seconds = (process_time_ns() - start) / 1_000_000_000
            elapsed = total_cpu_seconds / runs
            if matching is None or len(matching) != size:
                raise RuntimeError(f"{algorithm_name} did not return a complete matching")
            runtimes.append(elapsed)
            print(f"  CPU seconds per run: {elapsed:.9f} (runs: {runs})", flush=True)
            del first, second, matching
        average_time = sum(runtimes) / len(runtimes)
        average_times[size] = average_time
        print(f"n={size}, average CPU seconds: {average_time:.9f}\n", flush=True)

    print(f"{algorithm_name} average runtimes:", flush=True)
    print("Group size | Average CPU seconds", flush=True)
    for size, average_time in average_times.items():
        print(f"{size:10d} | {average_time:.9f}", flush=True)


def main():
    benchmark("gale_shapley", gale_shapley, GROUP_SIZES_A,
              instances=INSTANCES_PER_SIZE, seed=SEED)
    from brute_force import find_matches
    benchmark("brute_force", find_matches, GROUP_SIZES_B,
              instances=INSTANCES_PER_SIZE, seed=SEED)


if __name__ == "__main__":
    main()
