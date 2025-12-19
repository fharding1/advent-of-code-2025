import math

def dist(a,b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)

def connected_components(adj):
    components = []
    identified = []

    for i in range(len(adj)):
        if i in identified:
            continue
        res = dfs(adj, set(), i)
        identified += res
        components += [res]

    return components

def dfs(adj, visited, i):
    visited.update([i])
    for j in range(len(adj)):
        if j in visited:
            continue
        if adj[i][j]:
            visited.update(dfs(adj, visited, j))
    return visited


with open("input", "r") as file:
    coords = []
    for line in file:
        coords.append([int(x) for x in line.strip().split(',')])

    dists = []
    for i in range(len(coords)):
        for j in range(i+1,len(coords)):
            dists.append((i,j,dist(coords[i],coords[j])))
    
    dists = sorted(dists, key = lambda x : x[2])

    adj = [[0 for _ in coords] for _ in coords]

    for k in range(1000):
        (i,j,d) = dists.pop(0)
        adj[i][j] = 1
        adj[j][i] = 1

    # components = connected_components(adj)
    # component_sizes = [len(component) for component in components]
    # component_sizes.sort(reverse=True)
    # print(component_sizes[0] * component_sizes[1] * component_sizes[2])

    components = connected_components(adj)
    last = (0,0,0)
    while len(components) != 1:
        (i,j,d) = dists.pop(0)
        last = (i,j,d)
        component_i = 0
        component_j = 0
        for k in range(len(components)):
            if i in components[k]:
                component_i = k
            if j in components[k]:
                component_j = k
        components[component_i].update(components[component_j])
        if component_i != component_j:
            del components[component_j]
    
    (i,j,d) = last
    print(coords[i][0]*coords[j][0])
