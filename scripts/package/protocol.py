from __future__ import annotations

from typing import List, TypedDict


__all__ = ("SolutionJSON",)


class SolutionJSON(TypedDict):
    problem: str
    trucks_count: int
    drones_count: int
    iterations: int
    tabu_size: int
    config: str
    speed_type: str
    range_type: str
    cost: float
    capacity_violation: float
    drone_energy_violation: float
    fixed_time_violation: float
    fixed_distance_violation: float
    truck_paths: List[List[List[int]]]
    drone_paths: List[List[List[int]]]
    feasible: bool
    last_improved: int
    real: float
    user: float
    sys: float
