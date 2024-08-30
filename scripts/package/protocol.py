from __future__ import annotations

from typing_extensions import Dict, Generic, List, Tuple, TypedDict, TypeVar


__all__ = (
    "SolutionJSON",
    "PrettySolutionJSON",
    "PropagationJSON",
    "NeighborhoodJSON",
    "HistoryJSON",
    "ProgressJSON",
    "ResultJSON",
    "MILPResultJSON",
    "prettify"
)


class _BaseSolutionJSON(TypedDict):
    cost: float
    working_time: float
    drone_energy_violation: float
    capacity_violation: float
    waiting_time_violation: float
    fixed_time_violation: float
    fixed_distance_violation: float
    feasible: bool


T = TypeVar("T", bound=_BaseSolutionJSON)


class SolutionJSON(_BaseSolutionJSON):
    truck_paths: List[List[List[int]]]
    drone_paths: List[List[List[int]]]


class PrettySolutionJSON(_BaseSolutionJSON):
    truck_paths: str
    drone_paths: str


class PropagationJSON(Generic[T], TypedDict):
    solution: T
    label: str


class HistoryJSON(Generic[T], TypedDict):
    solution: T
    iteration: int
    penalty_coefficients: List[float]


class ProgressJSON(Generic[T], TypedDict):
    solution: T
    penalty_coefficients: List[float]


class NeighborhoodJSON(TypedDict):
    label: str
    pair: Tuple[int, int]


class ResultJSON(Generic[T], TypedDict):
    problem: str
    trucks_count: int
    drones_count: int
    iterations: int
    tabu_size: int
    config: str
    speed_type: str
    range_type: str
    solution: T
    propagation: List[PropagationJSON[T]]
    history: List[HistoryJSON[T]]
    progress: List[ProgressJSON[T]]
    neighborhoods: List[NeighborhoodJSON]
    initialization_label: str
    last_improved: int
    elite_set: List[List[float]]
    elite_set_extraction: List[int]
    real: float
    user: float
    sys: float


class MILPResultJSON(TypedDict):
    x: Dict[str, float]
    y: Dict[str, float]
    L_w: float
    L_d: float
    staff_velocity: float
    drone_velocity: float
    num_staff: int
    num_drone: int
    use_ejection: bool
    use_inter: bool
    use_intra: bool
    Optimal: float
    Solve_Time: float
    status: str


def prettify(solution: SolutionJSON) -> PrettySolutionJSON:
    return {
        **solution,
        "truck_paths": str(solution["truck_paths"]),
        "drone_paths": str(solution["drone_paths"]),
    }
