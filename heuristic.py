from maps import Location
#I have chosen manhattan distance as a heuristic function. 

#I chose manhattan over euclidean as the agent in this problem
#cannot navigate diagonally, only in four directions (in the
#same manner manhattan distance travels). 

#This function is consistent as path costs will never be overestimated and will always be less than
#or equal to the estimated path cost from any neighboring location to
#the goal, plus the actual path cost of reaching the neighbor

#actual terrain difficulty is 1 or greater, this function uses 1 for each
#'manhattan block' so it cannot overestimate

def heuristic(a: Location, b: Location):
   (x1, y1) = a
   (x2, y2) = b
   
   return abs(x1 - x2) + abs(y1 - y2)

