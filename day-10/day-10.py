# https://adventofcode.com/2019/day/9

import numpy as np

def clean_input(path="./input.txt"):
    input_f = open(path).readlines()
    return np.vstack([[True if e == '#' else False for e in line.strip()] for line in input_f])

def max_seen(mat):
    asteroid_pos = np.argwhere(mat)
    seen = []
    for asteroid in asteroid_pos:
        seen_angles = set()
        seen.append(0)
        for other in asteroid_pos:
            if (asteroid == other).all():
                continue

            diff = asteroid - other
            angle = np.angle(np.complex(diff[0], diff[1]))

            if angle not in seen_angles:
                seen_angles.add(angle)
                seen[-1] += 1

    return max(seen), asteroid_pos[np.argmax(seen)]

def second_star(mat, station=None):
    if station is None:
        station = max_seen(mat)[1]

    asteroid_pos = np.argwhere(mat)

    asteroid_with_coeff = []
    for other in asteroid_pos:
        if (station == other).all():
            continue
        diff = station - other
        x = diff[1]
        y = diff[0]
        # Rotate by 90 degrees so that UP is the 0° coord
        angle = np.angle(np.complex(y, -x))
        # Turn angles into absolutes
        absangle = (angle + 2 * np.pi) % (2 * np.pi)

        asteroid_with_coeff.append([other, absangle])

    ordered = sorted(asteroid_with_coeff, key=lambda t: (
        t[1], np.linalg.norm(t[0] - station)))

    seen = []
    # Remove duplicates while keeping order
    angles = list(dict.fromkeys(map(lambda t: t[1], ordered)))
    grouped_by_angle = [list(map(lambda t: t[0], filter(
        lambda t: t[1] == angle, ordered))) for angle in angles]
    rotations = 0
    while len(seen) < 200:
        for group in grouped_by_angle:
            if len(group) > rotations:
                current = group[rotations]
                seen.append(current)
        rotations += 1

    n_200 = seen[199]
    return n_200[1]*100 + n_200[0]

if __name__ == "__main__":
    mat = clean_input()
    station = max_seen(mat)
    print(f"First star answer: {station[0]}")
    print(f"Second star answer: {second_star(mat, station[1])}")
