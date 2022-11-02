import numpy as np

Location = tuple[int,int]
Map = np.ndarray


def read_map(file_name: str) -> Map:
    return np.loadtxt(file_name, dtype=int)

def cost(terrain_map: Map, from_node: Location, to_node: Location) -> int:
    
    from_first_index = from_node[0]
    from_second_index = from_node[1]
    
    to_first_index = to_node[0]
    to_second_index = to_node[1]
  
    first_cost = terrain_map[from_first_index][from_second_index]
    second_cost = terrain_map[to_first_index][to_second_index]
    
    return first_cost + second_cost

def safe_probability(success_map: Map, to_node: Location) -> float:
    
    to_first_index = to_node[0]
    to_second_index = to_node[1]
    
    capture_prob_val = success_map[to_first_index][to_second_index]
    capture_prob = 1 - capture_prob_val / 100

    return capture_prob
  
    
