import click
from typing import Optional
from events import log_visit_state, log_enqueue_state, log_ignore_state, log
from maps import Location, Map, cost
from parsing import validate_location, validate_map
import queue
from heuristic import heuristic
from find_neighbours import find_neighbours

def find_shortest_path(start: Location, goal: Location, 
                       terrain_map: Map, terrain_threshold: int) \
                   -> tuple[Optional[int],Optional[list[Location]]]:
    """Finds the path with lowest total cost (Task 1)
       Returns (cost,list(locations)) when a path is found.
       Returns (None,None) if no path is found."""

    
    allNeighbors = find_neighbours(terrain_map, terrain_threshold)
    
    frontier = queue.PriorityQueue()
    frontier.put((0, start))
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, int] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        
       current = frontier.get()
       log_visit_state(current[1], cost_so_far[current[1]]) #log event
       
       if current[1] == goal:
            
           break #goal found
       
       for next in allNeighbors:
           
           if(next["x"] == current[1][0] and next["y"] == current[1][1]):
               
               for neighbor in next["neighbors"]:
                   
                   new_cost = cost_so_far[current[1]] + cost(terrain_map, current[1], neighbor)
               
                   if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                     
                       cost_so_far[neighbor] = new_cost
                       priority = new_cost + heuristic(neighbor, goal) #compute priority for frontier
                       frontier.put((priority, neighbor))
                       log_enqueue_state(neighbor, new_cost) #log event
                       
                       came_from[neighbor] = current[1]
                       
                   else:
                       
                       log_ignore_state(neighbor, cost_so_far[neighbor]) #log event
    
    #init path and construct from breadcrumbs left in came_from dict
    new_path = []
        
    for target in came_from:
        
        if target == goal:
            
            new_path.append(target)
            prev = came_from[target]
            
            length = len(came_from)
            i = 0
            
            while i < length:
            
                new_path.append(prev)
                prev = came_from[prev]
                
                #follow the breadcrumb path
                if prev == start:
                    new_path.append(prev)
                    break
                i += 1
        
    new_path.reverse() 
    
    #constructed path must have more than one location
    if len(new_path) > 1:
    
        return cost_so_far[current[1]], new_path
    
    else:
        
        new_path = None


@click.command(no_args_is_help=True)
@click.argument('start', required=True, callback=validate_location)
@click.argument('goal', required=True, callback=validate_location)
@click.argument("terrain_map", required=True, type=click.Path(exists=True), callback=validate_map)
@click.argument("terrain_threshold", required=True, type=click.IntRange(min=0,max=1000))
def main(start: Location, goal: Location, terrain_map: Map, terrain_threshold: int) -> None:
    
    
    """Example usage:

    \b
    python pathfinding_task1.py 3,2 0,3 resources/terrain01.txt 50
    """
    path = find_shortest_path(start, goal, terrain_map, terrain_threshold)
    if path:
        log(f"The path is {path[1]} with cost {path[0]}.")
    else:
        log('No path found')

if __name__ == '__main__':
    main()
