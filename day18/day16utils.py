def dijkstras(grid, start, end):
    height = len(grid)
    width = len(grid[0])
    
    examined = set() # checked nodes
    completed_routes = []
    fringe = [(start, [start], 0)]
    visited = {} # contains the shortest distance to a node
    visited[start] = 0

    while fringe:
        u, path, distance = fringe.pop(0)
        
        # Check if we have reached the end
        if u == end:
            completed_routes.append((path + [end], distance))
            continue
        
        #visited[u] = distance
        examined.add(u)
        
        for shift in [(0, -1),  (0, 1), (1, 0), (-1, 0)]:
            nx = u[0] + shift[0]
            ny = u[1] + shift[1]
            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue
            
            potential = (nx, ny)
            if potential not in examined:
                if grid[ny][nx] == "#":
                    continue
                
                if potential not in visited or visited[potential] > distance + 1:
                    visited[potential] = distance + 1
                    fringe.append((potential, path + [u], distance + 1))
                
    if len(completed_routes) == 0:
        return None, None
    
    return completed_routes[-1][1], completed_routes

def print_route(grid, path, start, end):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) in path:
                print("O", end="")
            else:
                print(grid[y][x], end="")
        print()