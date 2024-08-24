from __future__ import annotations

import argparse
import sys
from typing_extensions import Literal, TYPE_CHECKING

from package import DroneEnduranceConfig, DroneLinearConfig, DroneNonlinearConfig, Problem, TruckConfig


class Namespace(argparse.Namespace):
    if TYPE_CHECKING:
        problem: str
        iterations: int
        tabu_size: int
        config: Literal["linear", "non-linear", "endurance"]
        speed_type: Literal["low", "high"]
        range_type: Literal["low", "high"]
        verbose: bool


parser = argparse.ArgumentParser(
    description="The min-timespan parallel technician-and-drone scheduling in door-to-door sampling service system.\nAlgorithm input transformer.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("problem", type=str, help="the problem name in the archive")
parser.add_argument("-i", "--iterations", default=1200, type=int, help="the number of iterations to run the algorithm for")
parser.add_argument("-t", "--tabu-size", default=10, type=int, help="the tabu size for each neighborhood")
parser.add_argument("-c", "--config", default="linear", choices=["linear", "non-linear", "endurance"], help="the energy consumption model to use")
parser.add_argument("--speed-type", default="low", choices=["low", "high"], help="speed type of drones")
parser.add_argument("--range-type", default="low", choices=["low", "high"], help="range type of drones")
parser.add_argument("-v", "--verbose", action="store_true", help="the verbose mode")


if __name__ == "__main__":
    namespace = Namespace()
    parser.parse_args(namespace=namespace)

    print(namespace, file=sys.stderr)

    problem = Problem.import_data(namespace.problem)
    print(problem.customers_count, problem.trucks_count, problem.drones_count)

    print(*problem.x)
    print(*problem.y)
    print(*problem.demands)
    print(*map(int, problem.dronable))

    print(*problem.truck_service_time)
    print(*problem.drone_service_time)

    print(namespace.iterations)
    print(namespace.tabu_size)
    print(int(namespace.verbose))

    truck = TruckConfig(maximum_velocity=problem.truck_speed, capacity=problem.truck_capacity, coefficients=(1,))
    print(truck.maximum_velocity, truck.capacity)
    print(len(truck.coefficients), *truck.coefficients)

    model = DroneEnduranceConfig(
        capacity=problem.drone_capacity,
        speed_type="low",
        range_type="low",
        fixed_time=problem.drone_endurance,
        fixed_distance=10 ** 9,
        drone_speed=problem.drone_speed,
    )

    print(model.__class__.__name__)
    print(
        model.capacity,
        model.speed_type,
        model.range_type,
    )
    if isinstance(model, DroneLinearConfig):
        print(
            model.takeoff_speed,
            model.cruise_speed,
            model.landing_speed,
            model.altitude,
            model.battery,
            model.beta,
            model.gamma,
        )
    elif isinstance(model, DroneNonlinearConfig):
        print(
            model.takeoff_speed,
            model.cruise_speed,
            model.landing_speed,
            model.altitude,
            model.battery,
            model.k1,
            model.k2,
            model.c1,
            model.c2,
            model.c4,
            model.c5,
        )
    else:
        print(
            model.fixed_time,
            model.fixed_distance,
            model.drone_speed,
        )

    print(
        problem.truck_time_limit,
        problem.drone_time_limit,
        problem.truck_unit_cost,
        problem.drone_unit_cost,
    )
