def find_neighbours(arr, terrain_threshold):

    neighbors = []

    for i in range(len(arr)):
        
        for j, value in enumerate(arr[i]):
       
            # corner locations
            if i == 0 or i == len(arr) - 1 or j == 0 or j == len(arr[i]) - 1:
                
                new_neighbors = {} 
                
                if i != 0:
                    if(arr[i - 1][j] < terrain_threshold):
                        
                        tempVal = arr[i - 1][j] #top neighbor value
                        tempLocation = (i-1 , j) #top neighbor x y
                        
                        new_neighbors[tempLocation] = tempVal
                       
                
                if j != len(arr[i]) - 1:
                    if(arr[i][j + 1] < terrain_threshold):
                        
                        tempVal = arr[i][j + 1] #right neighbor value
                        tempLocation = (i , j + 1) #right neighbor x y
                       
                        new_neighbors[tempLocation] = tempVal
                       
                
                if i != len(arr) - 1:
                    if(arr[i + 1][j] < terrain_threshold):
                        
                        tempVal = arr[i + 1][j] #bottom neighbor value
                        tempLocation = (i + 1, j) #bottom neighbor x y
                        new_neighbors[tempLocation] = tempVal
                        
                
                if j != 0:
                    if(arr[i][j - 1] < terrain_threshold):
                        
                        tempVal = arr[i][j - 1] #left neighbor value
                        tempLocation = (i, j - 1) #left neighbor x y
                        new_neighbors[tempLocation] = tempVal
                        

            else:
                
                new_neighbors = {}
                
                
                if(arr[i - 1][j] < terrain_threshold):
                    tempVal = arr[i - 1][j] #top neighbor value
                    tempLocation = (i - 1, j) #top neighbor x y
                    new_neighbors[tempLocation] = tempVal
                   
                
                if(arr[i][j + 1] < terrain_threshold): 
                    tempVal = arr[i][j + 1] #right neighbor value
                    tempLocation = (i, j + 1) #right neighbor x y
                    new_neighbors[tempLocation] = tempVal
                   
                   
                if(arr[i + 1][j] < terrain_threshold): 
                    tempVal = arr[i + 1][j] #bottom neighbor value
                    tempLocation = (i + 1, j) #bottom neighbor x y
                    new_neighbors[tempLocation] = tempVal
                   
                   
                if(arr[i][j - 1] < terrain_threshold): 
                   tempVal = arr[i][j - 1] #left neighbor value
                   tempLocation = (i, j - 1) #left neighbor x y
                   new_neighbors[tempLocation] = tempVal
               
                
               

            neighbors.append({
                
                "x": i,
                "y": j,
                "value": value,
                "neighbors": new_neighbors
                
                })

    return neighbors

