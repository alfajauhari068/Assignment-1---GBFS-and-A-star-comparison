import heapq
import time

def find_start_goal(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'G':
                goal = (i, j)
    return start, goal

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def gbfs(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])
    open_heap = []
    heapq.heappush(open_heap, (heuristic(start, goal), start[0], start[1]))
    came_from = {}
    visited = set([start])
    nodes_explored = 0

    while open_heap:
        nodes_explored += 1
        h, row, col = heapq.heappop(open_heap)
        current = (row, col)

        if current == goal:
            break

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            next_node = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] != '#' and next_node not in visited:
                    priority = heuristic(next_node, goal)
                    heapq.heappush(open_heap, (priority, nr, nc))
                    came_from[next_node] = current
                    visited.add(next_node)

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return [], nodes_explored
    path.append(start)
    path.reverse()
    return path, nodes_explored

def a_star(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])
    open_heap = []
    heapq.heappush(open_heap, (0 + heuristic(start, goal), 0, start[0], start[1]))
    came_from = {}
    cost_so_far = {start: 0}
    nodes_explored = 0

    while open_heap:
        nodes_explored += 1
        f, g, row, col = heapq.heappop(open_heap)
        current = (row, col)

        if current == goal:
            break

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            next_node = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                new_g = g + 1
                if next_node not in cost_so_far or new_g < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_g
                    priority = new_g + heuristic(next_node, goal)
                    heapq.heappush(open_heap, (priority, new_g, nr, nc))
                    came_from[next_node] = current

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return [], nodes_explored
    path.append(start)
    path.reverse()
    return path, nodes_explored

def visualize_path(grid, path):
    grid_copy = [list(row) for row in grid]
    for (r, c) in path:
        if grid_copy[r][c] not in ('S', 'G'):
            grid_copy[r][c] = '*'
    for row in grid_copy:
        print(''.join(row))

def run_comparison(grid_str):
    grid = [row.strip() for row in grid_str]
    start, goal = find_start_goal(grid)
    
    # GBFS
    start_time = time.time()
    gbfs_path, gbfs_nodes = gbfs(grid, start, goal)
    gbfs_time = time.time() - start_time
    
    # A*
    start_time = time.time()
    astar_path, astar_nodes = a_star(grid, start, goal)
    astar_time = time.time() - start_time
    
    print("GBFS Path:")
    visualize_path(grid, gbfs_path)
    print("\nA* Path:")
    visualize_path(grid, astar_path)
    
    print("\nComparison:")
    print(f"GBFS - Time: {gbfs_time:.4f}s, Path Length: {len(gbfs_path)}, Nodes Explored: {gbfs_nodes}")
    print(f"A*   - Time: {astar_time:.4f}s, Path Length: {len(astar_path)}, Nodes Explored: {astar_nodes}")

# Contoh grid (pastikan semua baris memiliki panjang yang sama)
grid_str = [
    "S..#......",
    ".#.#.###..",
    ".#......#.",
    ".####.#...",
    ".....#.#G",
    "####.#.#..",
    "....#.#...",
    ".#.#.###..",
    ".#........",
    ".....####."
]

if __name__ == "__main__":
    run_comparison(grid_str)