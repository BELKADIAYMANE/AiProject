import numpy as np
import time
from fifteenpuzzle import FifteenPuzzleState, h1, h2, h3, h4
from search import aStarSearch

def parse_puzzle_state(scenario):
    puzzle_list = list(map(int, scenario.split()))
    return FifteenPuzzleState(np.array(puzzle_list).reshape((4, 4)))

def run_experiments(scenarios, heuristics):
    results = []
    for scenario in scenarios:
        initial_state = parse_puzzle_state(scenario)
        for h_name, heuristic in heuristics.items():
            start_time = time.time()
            result = aStarSearch(initial_state, heuristic)
            end_time = time.time()
            
            execution_time = end_time - start_time
            results.append({
                'heuristic': h_name,
                'initial_state': scenario,
                'max_fringe_size': result.max_fringe_size,
                'expanded_nodes': result.expanded_nodes,
                'execution_time': execution_time,
                'solved': result.solved,
                'solution_depth': result.solution_depth
            })
    return results

if __name__ == "__main__":
    # Load scenarios
    with open("scenarios.csv", "r") as f:
        scenarios = f.read().strip().splitlines()

    heuristics = {
        'h1': h1,
        'h2': h2,
        'h3': h3,
        'h4': h4,
    }

    results = run_experiments(scenarios, heuristics)

    # Save results to results.csv
    with open("results.csv", "w") as f:
        f.write("heuristic,initial_state,max_fringe_size,expanded_nodes,execution_time,solved,solution_depth\n")
        for result in results:
            f.write(f"{result['heuristic']},{result['initial_state']},{result['max_fringe_size']},"
                    f"{result['expanded_nodes']},{result['execution_time']},{result['solved']},"
                    f"{result['solution_depth']}\n")
