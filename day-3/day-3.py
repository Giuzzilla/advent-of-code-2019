#https://adventofcode.com/2019/day/3

def clean_input(path = "./input.txt"):
    input_f = open(path).readlines()
    return [el.strip().split(',') for el in input_f]

def common_points(arr):
    central_port = (0, 0) # Points need to be tuples, otherwise not hashable.
    points = [[(0, 0)], [(0, 0)]] # Keep them in lists as to keep the order (useful for second star)
    for i, wire in enumerate(arr):
        for move in wire:
            dire = move[:1]
            move_size = int(move[1:])
            if dire == 'R':
                for _ in range(move_size):
                    points[i].append((points[i][-1][0], points[i][-1][1] + 1))
            elif dire == 'D':
                for _ in range(move_size):
                    points[i].append((points[i][-1][0] - 1, points[i][-1][1]))
            elif dire == 'L':
                for _ in range(move_size):
                    points[i].append((points[i][-1][0], points[i][-1][1] - 1))
            elif dire == 'U':
                for _ in range(move_size):
                    points[i].append((points[i][-1][0] + 1, points[i][-1][1]))
    
    points_1 = set(points[0])
    points_2 = set(points[1])
    common = points_1.intersection(points_2).difference(set([central_port])) # get common points excluding the central port

    return common, points

def first_star(common):
    dists = []
    for point in common:
        dists.append(manhattan_distance((0, 0), point))
    return min(dists)


def second_star(common, points):
    dists = []
    for p in common:
        dists.append(points[1].index(p) + points[0].index(p))
    return min(dists)


def manhattan_distance(point1, point2):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])

if __name__ == "__main__":
    common, points = common_points(clean_input())
    print(f"First star answer: {first_star(common)}")
    print(f"Second star answer: {second_star(common, points)}")
