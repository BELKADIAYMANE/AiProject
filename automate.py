import search
import csv
import concurrent.futures
from fifteenpuzzle import (
    createRandomFifteenPuzzle,
    FifteenPuzzleState,
    is_solvable,
    FifteenPuzzleSearchProblem,
    h1,
    h2,
    h3,
    h4,
)


def read_puzzles_from_csv(filename="scenarios.csv"):
    puzzles = []
    with open(filename, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            puzzle = list(map(int, row))
            puzzles.append(FifteenPuzzleState(puzzle))
    return puzzles


def write_results_to_csv(results, filename="results.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Result", "Depth", "Expanded Nodes", "Max Fringe Size"])  # Write header
        for result in results:
            writer.writerow(result)


def generate_random_puzzles(num_puzzles=500):
    puzzles = []
    for _ in range(num_puzzles):
        puzzle = createRandomFifteenPuzzle(25)
        flattened_puzzle = [tile for row in puzzle.cells for tile in row]
        puzzles.append(flattened_puzzle)
    print("generated random puzzles")
    return puzzles


def solve_puzzle(puzzle):
    if is_solvable(puzzle):
        problem = FifteenPuzzleSearchProblem(puzzle)
        
        # Run the search and capture additional metrics
        path, expanded_nodes, max_fringe_size = search.aStarSearch(problem, h1)
        depth_of_solution = len(path)
        
        result = f"A* found a path of {depth_of_solution} moves"
        
        misplaced_tiles = h1(puzzle)
        print(f"Heuristic 1 gives: {misplaced_tiles}")

        # Calculate and display the Euclidean distance
        euclidean_distance = h2(puzzle)
        print(f"Heuristic 2 gives: {euclidean_distance}")

        # Calculate and display the Manhattan distance
        manhattan_distance = h3(puzzle)
        print(f"Heuristic 3 gives: {manhattan_distance}")

        # Calculate and display the Out of row/column heuristic
        out_of_row, out_of_column = h4(puzzle)
        print(f"Heuristic 4 gives: {out_of_row + out_of_column}")
        
        return (result, depth_of_solution, expanded_nodes, max_fringe_size)
    else:
        result = "not solvable"
        return (result, None, None, None)


def write_puzzles_to_csv(puzzles, filename="scenarios.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Tile" + str(i) for i in range(1, 17)])
        writer.writerows(puzzles)


if __name__ == "__main__":

    # Generate random puzzles and write them to CSV
    config = generate_random_puzzles()
    write_puzzles_to_csv(config)

    # Read puzzles from CSV
    puzzles = read_puzzles_from_csv()

    # Solve each puzzle in parallel
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(solve_puzzle, puzzles))

    # Write results to CSV
    write_results_to_csv(results)
    print("Results have been written to results.csv")
