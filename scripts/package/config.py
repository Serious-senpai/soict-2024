from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Final, List, Literal, Tuple


__all__ = ("ROOT", "TruckConfig", "DroneLinearConfig", "DroneNonlinearConfig", "DroneEnduranceConfig", "Problem")
ROOT: Final[Path] = Path(__file__).parent.parent.parent


@dataclass(frozen=True, kw_only=True, slots=True)
class TruckConfig:
    maximum_velocity: float
    capacity: float
    coefficients: Tuple[float, ...]

    @staticmethod
    def import_data() -> TruckConfig:
        with open(ROOT / "problems" / "config_parameter" / "truck_config.json", "r") as file:
            data = json.load(file)

        coefficients_d = data["T (hour)"]
        assert isinstance(coefficients_d, dict)

        return TruckConfig(
            maximum_velocity=data["V_max (m/s)"],
            capacity=data["M_t (kg)"],
            coefficients=tuple(coefficients_d.values()),
        )


@dataclass(frozen=True, kw_only=True, slots=True)
class _BaseDroneConfig:
    capacity: float
    speed_type: Literal["low", "high"]
    range_type: Literal["low", "high"]


@dataclass(frozen=True, kw_only=True, slots=True)
class _VariableDroneConfig(_BaseDroneConfig):
    takeoff_speed: float
    cruise_speed: float
    landing_speed: float
    altitude: float
    battery: float

    @staticmethod
    def from_data(data: Dict[str, Any]) -> _VariableDroneConfig:
        return _VariableDroneConfig(
            takeoff_speed=data["takeoffSpeed [m/s]"],
            cruise_speed=data["cruiseSpeed [m/s]"],
            landing_speed=data["landingSpeed [m/s]"],
            altitude=data["cruiseAlt [m]"],
            battery=data["batteryPower [Joule]"],
            capacity=data["capacity [kg]"],
            speed_type=data["speed_type"],
            range_type=data["range"],
        )


@dataclass(frozen=True, kw_only=True, slots=True)
class DroneLinearConfig(_VariableDroneConfig):
    beta: float
    gamma: float

    @staticmethod
    def import_data() -> Tuple[DroneLinearConfig, ...]:
        with open(ROOT / "problems" / "config_parameter" / "drone_linear_config.json", "r") as file:
            data = json.load(file)
            assert isinstance(data, dict)

        results: List[DroneLinearConfig] = []
        for d in data.values():
            base = _VariableDroneConfig.from_data(d)
            item = DroneLinearConfig(
                beta=d["beta(w/kg)"],
                gamma=d["gamma(w)"],
                **asdict(base),
            )

            results.append(item)

        return tuple(results)


@dataclass(frozen=True, kw_only=True, slots=True)
class DroneNonlinearConfig(_VariableDroneConfig):
    k1: float
    k2: float
    c1: float
    c2: float
    c4: float
    c5: float

    @staticmethod
    def import_data() -> Tuple[DroneNonlinearConfig, ...]:
        with open(ROOT / "problems" / "config_parameter" / "drone_nonlinear_config.json", "r") as file:
            data = json.load(file)
            assert isinstance(data, dict)

        results: List[DroneNonlinearConfig] = []
        for d in data.values():
            if isinstance(d, dict):
                base = _VariableDroneConfig.from_data(d)
                item = DroneNonlinearConfig(
                    k1=data["k1"],
                    k2=data["k2 (sqrt(kg/m)"],
                    c1=data["c1 (sqrt(m/kg)"],
                    c2=data["c2 (sqrt(m/kg)"],
                    c4=data["c4 (kg/m)"],
                    c5=data["c5 (Ns/m)"],
                    **asdict(base),
                )

                results.append(item)

        return tuple(results)


@dataclass(frozen=True, kw_only=True, slots=True)
class DroneEnduranceConfig(_BaseDroneConfig):
    fixed_time: float
    fixed_distance: float
    drone_speed: float

    @staticmethod
    def import_data() -> Tuple[DroneEnduranceConfig, ...]:
        with open(ROOT / "problems" / "config_parameter" / "drone_endurance_config.json", "r") as file:
            data = json.load(file)
            assert isinstance(data, dict)

        results: List[DroneEnduranceConfig] = []
        for d in data.values():
            item = DroneEnduranceConfig(
                fixed_time=d["FixedTime (s)"],
                fixed_distance=d["FixedDistance (m)"],
                drone_speed=d["Drone_speed (m/s)"],
                capacity=d["capacity [kg]"],
                speed_type=d["speed_type"],
                range_type=d["range"],
            )

            results.append(item)

        return tuple(results)


@dataclass(frozen=True, kw_only=True, slots=True)
class Problem:
    problem: str
    customers_count: int
    trucks_count: int
    drones_count: int

    x: Tuple[float, ...]
    y: Tuple[float, ...]
    demands: Tuple[float, ...]
    dronable: Tuple[bool, ...]

    truck_service_time: Tuple[float, ...]
    drone_service_time: Tuple[float, ...]

    truck_capacity: float

    @staticmethod
    def import_data(problem: str, /) -> Problem:
        problem = problem.removesuffix(".vrp")

        customers_count = 0
        trucks_count = drones_count = 1
        if problem == "CMT1":
            customers_count = 50
            trucks_count = 3
            drones_count = 2

        elif problem == "CMT2":
            customers_count = 75
            trucks_count = drones_count = 5

        elif problem == "CMT3":
            customers_count = 100
            trucks_count = drones_count = 4

        elif problem == "CMT4":
            customers_count = 150
            trucks_count = drones_count = 6

        elif problem == "CMT5":
            customers_count = 199
            trucks_count = 9
            drones_count = 8

        with ROOT.joinpath("problems", "cvrplib", f"{problem}.vrp").open("r") as file:
            data = file.read()

        x: List[float] = []
        y: List[float] = []
        demands: List[float] = []
        dronable = [True] * (1 + customers_count)
        truck_service_time = [0.0] * (1 + customers_count)
        drone_service_time = [0.0] * (1 + customers_count)

        for match in re.finditer(r"^(\d+)\s+(\d+(?:\.\d*)?)\s+(\d+(?:\.\d*)?)$", data, re.MULTILINE):
            _, _x, _y = match.groups()
            x.append(float(_x))
            y.append(float(_y))

        for match in re.finditer(r"^(\d+)\s+(\d+(?:\.\d*)?)$", data, re.MULTILINE):
            _, _demand = match.groups()
            demands.append(float(_demand))

        truck_capacity = float(re.search(r"^CAPACITY : (\d+(?:\.\d*)?)$", data, re.MULTILINE).group(1))  # type: ignore

        return Problem(
            problem=problem,
            customers_count=customers_count,
            trucks_count=trucks_count,
            drones_count=drones_count,
            x=tuple(x),
            y=tuple(y),
            demands=tuple(demands),
            dronable=tuple(dronable),
            truck_service_time=tuple(truck_service_time),
            drone_service_time=tuple(drone_service_time),
            truck_capacity=truck_capacity,
        )
