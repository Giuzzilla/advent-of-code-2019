from collections import defaultdict

def clean_input(path = '/home/giuzzilla/Desktop/advent-of-code-2019/day-6/input.txt'):
    input_f = open(path).readlines()
    return [el.strip().split(')') for el in input_f]

def create_dict(arr, unidirectional=True):
    orbit_dict = defaultdict(list)
    for orbit in arr:
        orbit_dict[orbit[1]].append(orbit[0]) 
        if not unidirectional: # Useful for second part with a BFS/DFS
            orbit_dict[orbit[0]].append(orbit[1])
    return orbit_dict

def root_find(graph, sink, root="COM"):
    path = [sink]
    while path[-1] != root:
        path.append(graph[path[-1]][0])
    return path

def first_star(arr):
    flat = map(lambda l: l[1], arr)

    orbit_dict = create_dict(arr)
    steps = 0
    for node in set(flat):
        steps += len(root_find(orbit_dict, node)) - 1

    return steps

# Despite this can be easily done with a BFS/DFS, this is also another possible solution.
# Possibly faster.
# Find the paths to root of YOU.
# Then do the same for SAN but stop at the first occurence of a node encountered
# in the path of YOU.
# Then join together the path of YOU (sliced up to the comomn point) with the
# inverted path of SAN.
def common_find(graph, sink, other_path):
    path = [sink]
    while path[-1] not in other_path:
        path.append(graph[path[-1]][0])
    return path

def second_star(arr, start_planet='YOU', end_planet='SAN'):
    orbit_dict = create_dict(arr)
    start = orbit_dict[start_planet][0]
    end = orbit_dict[end_planet][0]

    path1 = root_find(orbit_dict, start)
    path2 = common_find(orbit_dict, end, path1)

    joined_path = path1[:path1.index(path2[-1])]
    joined_path.extend(path2[::-1])

    return len(joined_path) - 1

if __name__ == "__main__":
    arr = clean_input()
    print(f"First star answer: {first_star(arr)}")
    print(f"Second star answer: {second_star(arr)}")
