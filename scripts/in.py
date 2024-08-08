from __future__ import annotations

import sys

from package import parser, DroneEnduranceConfig, DroneLinearConfig, DroneNonlinearConfig, Namespace, Problem, TruckConfig


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
