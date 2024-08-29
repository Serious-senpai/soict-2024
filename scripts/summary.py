from __future__ import annotations

import json
import re
from typing_extensions import Dict, List

from package import MILPResultJSON, ResultJSON, SolutionJSON, ROOT, csv_wrap


def compare() -> Dict[str, MILPResultJSON]:
    result: Dict[str, MILPResultJSON] = {}
    for file in ROOT.joinpath("problems", "milp").iterdir():
        match = re.search(r"\d+\.\d+\.\d+", file.name)
        if file.is_file() and file.name.endswith(".json") and match is not None:
            problem = match.group()
            with file.open("r") as f:
                data = json.load(f)

            result[problem] = MILPResultJSON(**data)  # type: ignore  # will throw at runtime if fields are incompatible

    return result


if __name__ == "__main__":
    ROOT.joinpath("result", "summary.json").unlink(missing_ok=True)

    results: List[ResultJSON[SolutionJSON]] = []
    for file in sorted(ROOT.joinpath("result").iterdir(), key=lambda f: f.name):
        if file.is_file() and file.name.endswith(".json") and not file.name.endswith("-pretty.json"):
            print(file.absolute())
            with file.open("r") as f:
                data = json.load(f)

            result = ResultJSON[SolutionJSON](**data)  # type: ignore  # will throw at runtime if fields are incompatible
            results.append(result)

    milp = compare()

    with ROOT.joinpath("result", "summary.csv").open("w") as csv:
        csv.write("sep=,\n")
        csv.write("Problem,Customers count,Trucks count,Drones count,Iterations,Tabu size,Energy model,Speed type,Range type,Cost,MILP cost,Improved [%],MILP performance,MILP status,Capacity violation,Energy violation,Waiting time violation,Fixed time violation,Fixed distance violation,Truck paths,Drone paths,Feasible,Initialization,Last improved,real,user,sys\n")
        for row, result in enumerate(results, start=2):
            milp_available = result["problem"] in milp
            segments = [
                csv_wrap(result["problem"]),
                csv_wrap(f"=VALUE(LEFT(A{row}, SEARCH(\"\".\"\", A{row}) - 1))"),
                str(result["trucks_count"]),
                str(result["drones_count"]),
                str(result["iterations"]),
                str(result["tabu_size"]),
                result["config"],
                result["speed_type"],
                result["range_type"],
                str(result["solution"]["cost"]),
                str(60 * milp[result["problem"]]["Optimal"]) if milp_available else "",
                csv_wrap(f"=ROUND(100 * (K{row} - J{row}) / K{row}, 2)"),
                str(milp[result["problem"]]["Solve_Time"]) if milp_available else "",
                str(milp[result["problem"]]["status"]) if milp_available else "",
                str(result["solution"]["capacity_violation"]),
                str(result["solution"]["drone_energy_violation"]),
                str(result["solution"]["waiting_time_violation"]),
                str(result["solution"]["fixed_time_violation"]),
                str(result["solution"]["fixed_distance_violation"]),
                csv_wrap(result["solution"]["truck_paths"]),
                csv_wrap(result["solution"]["drone_paths"]),
                str(int(result["solution"]["feasible"])),
                result["initialization_label"],
                str(result["last_improved"]),
                str(result["real"]),
                str(result["user"]),
                str(result["sys"]),
            ]
            csv.write(",".join(segments) + "\n")

    with ROOT.joinpath("result", "summary.json").open("w") as f:
        json.dump(results, f, indent=4)
