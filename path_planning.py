from typing import Set, Dict, Tuple, Optional, Sequence, List
import heapq
import math
import time

# This is how we write a type alias in Python
Map = List[List[str]]
# Now we can write load_map in terms of Map:
def load_map(mapfile:str) -> Map:
    with open(mapfile,encoding='utf-8') as infile:
        # This "list comprehension" is a very useful syntactic trick
        return [list(line.rstrip()) for line in infile]

# Example
terrain = load_map('terrain.txt')
print(terrain)

Point = Tuple[int, int]
# Now we can define our function in terms of Points
def find_neighbors(terrain:Map, p:Point) -> List[Tuple[Point, int]]:
    # Python has destructuring assignment.
    # You could just as well write `x = p[0]` and `y = p[1]`.
    x,y = p
    neighbors : List[Tuple[Point,int]] = []
    # A. Your code here...
    spaces: List[Point] = []
    if x > 0 and x < len(terrain) - 1: 
        spaces.append((x-1,y))
        spaces.append((x+1,y))
    elif x > 0: 
        spaces.append((x-1,y))
    elif x < len(terrain) - 1: 
        spaces.append((x + 1, y))

    if y > 0 and y < len(terrain[0]) - 1: 
        spaces.append((x,y-1))
        spaces.append((x,y+1))
    elif y > 0: 
        spaces.append((x, y - 1))
    elif y < len(terrain[0]) - 1: 
        spaces.append((x, y + 1))

    for i in range(len(spaces)): 
        a,b = spaces[i]
        if terrain[a][b] == '🌿' or terrain[a][b] == '🌉' or terrain[a][b] == '🌲':
            neighbors.append([spaces[i], 1])
        elif terrain[a][b] == '🌼': 
            neighbors.append([spaces[i], 2])
        else: 
            neighbors.append([spaces[i], 5]) 
    # Feel free to introduce other variables if they'd be helpful too.
    return neighbors


terrain = load_map('terrain.txt')
print(find_neighbors(terrain, (3,3)))

def pretty_print_path(terrain: Map, path: List[Point]):
    emojis = ['😀','😁','😂','🤣','😃','😄','😅','😆','😉','😊','😋']
    # This is a "dictionary comprehension" like the list comprehension above
    path2len = {location:distance for distance,location in enumerate(path)}
    output = []
    for yy,row in enumerate(terrain):
        row_str = ''
        for xx, cur in enumerate(row):
            if (xx,yy) in path2len:
                row_str += emojis[path2len[(xx,yy)] % len(emojis)]
            else:
                row_str += cur
        output.append(row_str)
    return '\\n'.join(output)

def print_search_result(terrain:Map, result:Tuple[int, int, Optional[List[Point]]]) -> None:
    print("Visited:",result[0])
    if result[2]:
        print("Best path cost:",result[1])
        print(pretty_print_path(terrain, result[2]))
    else:
        print("No path found")

def breadth_first(terrain:Map, start:Point, goal:Point) -> Tuple[int, int, Optional[List[Point]]]:
    open_list: List[Point] = [start]
    # We'll treat start specially
    best_costs: Dict[Point, Tuple[int, Point]] = {start:(0, start)}
    visit_count = 0
    while open_list:
        # Breadth-first search takes the first thing from the list...
        node = open_list.pop(0)
        visit_count += 1
        neighbors = find_neighbors(terrain, node)
        for neighbor, neighbor_cost in neighbors:
            # B. And does something with each neighbor node (where does the new node go in the list?)
            # Be sure to track the best cost and predecessor for each new node in `best_costs` too, and avoid re-expanding nodes which we've seen before with better costs. 
            parent_cost, parent = best_costs[node]
            if neighbor in best_costs: 
                prev_cost, predecessor = best_costs[neighbor]
                cost = parent_cost + neighbor_cost
                if prev_cost > cost: 
                    best_costs[neighbor] = cost, node
            else: 
                open_list.append(neighbor)
                cost = parent_cost + neighbor_cost
                best_costs[neighbor] = cost, node
            pass
        pass
    # C. If any path was found to goal, return the best such path.
    if goal in best_costs: 
        best_cost, goal_parent = best_costs[goal]
        return(visit_count, best_cost, goal_parent)
    else: 
    # Otherwise, return:
        return (visit_count, -1, None)


# # Example
terrain = load_map('terrain.txt')
print_search_result(terrain, breadth_first(terrain, (0, 0), (10, 0)))
print_search_result(terrain, breadth_first(terrain, (2, 3), (7, 0)))
print_search_result(terrain, breadth_first(terrain, (5, 5), (0, 1)))
print_search_result(terrain, breadth_first(terrain, (0, 0), (10, 9)))
print_search_result(terrain, breadth_first(terrain, (0, 0), (11, 10))) # out of bounds!