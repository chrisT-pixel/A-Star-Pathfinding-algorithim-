import click
from typing import Optional
from events import log_visit_state, log_enqueue_state, log_ignore_state, log
from maps import Location, Map, cost, safe_probability
from parsing import validate_location, validate_map
import queue
from heuristic import heuristic
from find_neighbors_enemy import find_neighbors_enemy

def find_shortest_safe_path(start: Location, goal: Location, 
                            terrain_map: Map, terrain_threshold: int,
                            success_map: Map, success_threshold: float) \
                            -> tuple[Optional[int],Optional[float],Optional[list[Location]]]:
    """Finds the path with lowest total cost that also satisfies 
       the minimum success probability threshold (Task 2).
       Returns (cost,prob_success,list(locations)) when a path is found.
       Returns (None,None,None) if no path is found."""
    
    allNeighbors = find_neighbors_enemy(terrain_map, terrain_threshold)
   
    frontier = queue.PriorityQueue()
    frontier.put((0, [start, 0, 1.0])) #init frontier with starting location, no cost, 100% prob
    came_from = {}
    came_from[start, 0, 1.0] = None #init came from with starting location, no cost, 100% prob
    
    #current[1][0] = location
    #current[1][1] = cost
    #current[1][2] = prob
    #neighbor[0] = location
    #neighbor[1][1] = cost
    #neighbor[1][2] = prob
     
    while not frontier.empty():
        
        current = frontier.get()
        log_visit_state(current[1][0], current[1][1], current[1][2]) #log event
        
        if current[1][0] == goal:
            
          break #goal found
        
        for next in allNeighbors:
            
            if(next["x"] == current[1][0][0] and next["y"] == current[1][0][1]):
                
                for neighbor in next["neighbors"].items(): 
                
                    new_cost = current[1][1] + cost(terrain_map, current[1][0], neighbor[0])
                    new_prob_safe = current[1][2] * safe_probability(success_map, neighbor[0])
        
                    if neighbor[1][1] == 0 or new_cost < neighbor[1][1] or new_prob_safe > neighbor[1][2]:
                   
                        if new_prob_safe >= success_threshold: #if prob is still acceptable put this neighbor back into frontier
                      
                            neighbor[1][1] = new_cost 
                            neighbor[1][2] = new_prob_safe
                            priority = new_cost + heuristic(neighbor[0], goal) #compute priority for frontier
                            frontier.put((priority, [neighbor[0], new_cost, new_prob_safe]))
                            log_enqueue_state(neighbor[0], new_cost, new_prob_safe) #log event
                            
                            #keep track of all to & from data
                            came_from[neighbor[0], neighbor[1][1], neighbor[1][2]] = (current[1][0], current[1][1], current[1][2])
                            
                            
                    else:
                        
                        log_ignore_state(neighbor[0], neighbor[1][1], neighbor[1][2]) #log event
                            
                           
                            
    #init path and construct from breadcrumbs left in came_from dict
    new_path = []
    startFound = False
    
    for target in came_from: 
         
         if target[0] == goal:
             
             new_path.append(target)
             prev = came_from[target]
             
             length = len(came_from)
             i = 0
             
             while i < length:
                 
                 if startFound == True:
                     break
             
                 new_path.append(prev)
                 prev = came_from[prev]
                 
                 
                 #follow the breadcrumb path
                 if prev[0] == start:
                     
                     new_path.append(prev)
                     startFound = True
                     break
                 i += 1
    
    new_path.reverse() 
    
    if len(new_path) > 1:
        
        while new_path[0][0] == goal: #if goal is in path more than once remove the first higher cost incorrect instance
            
            new_path.pop(0)
    
    stripped_path = []
   
    for location_data in new_path: #get location only, removing cost and probability
        stripped_path.append(location_data[0])
     
    #constructed path must have more than one location
    if len(new_path) > 1:
     
         return current[1][1], current[1][2], stripped_path
     
    else:
         
         new_path = None


@click.command(no_args_is_help=True)
@click.argument('start', required=True, callback=validate_location)
@click.argument('goal', required=True, callback=validate_location)
@click.argument("terrain_map", required=True, type=click.Path(exists=True), callback=validate_map)
@click.argument("terrain_threshold", required=True, type=click.IntRange(min=0,max=1000))
@click.argument("success_map", required=True, type=click.Path(exists=True), callback=validate_map)
@click.argument("success_threshold", required=True, type=click.FloatRange(min=0.0,max=1.0))
def main(start: Location, goal: Location, 
         terrain_map: Map, success_map: Map, 
         terrain_threshold: int, success_threshold: float) -> None:
    """Example usage:

        \b
        python safe_pathfinding_task2.py 3,2 0,3 resources/terrain01.txt 50 resources/enemy01.txt 1.0
    """
    path = find_shortest_safe_path(start, goal, terrain_map, terrain_threshold, success_map, success_threshold)
    if path:
        log(f"The path is {path[2]} with cost {path[0]} and success probability {path[1]}")
    else:
        log('No path found')

if __name__ == '__main__':
    main()
    
