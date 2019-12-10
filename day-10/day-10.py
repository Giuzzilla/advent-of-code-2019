#https://adventofcode.com/2019/day/9
import numpy as np
from itertools import zip_longest, islice


def clean_input(path="./day-10/input.txt"):
    input_f = open(path).readlines()
    return np.vstack([[True if e == '#' else False for e in line.strip()] for line in input_f])


def max_seen(asteroid_pos):
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
    
    station = asteroid_pos[np.argmax(seen)]
    return max(seen), station


def second_star(asteroid_pos, station):
    asteroid_with_coeff = []
    for other in asteroid_pos:
        if (station == other).all():
            continue

        diff = other - station
        x = diff[1]
        y = diff[0]
        # Rotate by 90 degrees so that UP is the 0° coord
        angle = np.angle(np.complex(-y, x))
        # Turn angles into [0, 2*pi] range
        absangle = (angle + 2 * np.pi) % (2 * np.pi)

        asteroid_with_coeff.append([other, absangle])

    ordered = sorted(asteroid_with_coeff, key=lambda t: (
        t[1], np.linalg.norm(t[0] - station)))

    seen = []
    # Remove duplicates while keeping order
    angles = list(dict.fromkeys(map(lambda t: t[1], ordered)))
    grouped_by_angle = [list(map(lambda t: t[0], filter(
        lambda t: t[1] == angle, ordered))) for angle in angles]

    # Zip lists of angles to have the correct progression
    # then flatten (and filter None-values)
    listed = [item for sublist in zip_longest(
        *grouped_by_angle) for item in sublist if item is not None]

    return listed[199][1]*100 + listed[199][0]

if __name__ == "__main__":
    mat = clean_input()
    positions = np.argwhere(mat)
    station = max_seen(positions)
    print(f"First star answer: {station[0]}")
    print(f"Second star answer: {second_star(positions, station[1])}")
