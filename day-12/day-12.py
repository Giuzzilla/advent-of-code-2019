#https://adventofcode.com/2019/day/12
import numpy as np
import math

def lcm(x, y):
    return (x * y) // math.gcd(x, y)

def clean_input(path="./input.txt"):
    input_f = open(path).readlines()
    return [line.strip()[1:-1].split(', ') for line in input_f]


def get_posvel(arr):
    pos = np.array([[int(item.split('=')[1]) for item in sublist] for sublist in arr], dtype=int)
    vel = np.zeros(shape=pos.shape, dtype=int)

    return pos, vel

def first_star(pos, vel):
    pos = pos.copy()
    vel = vel.copy()
    for _ in range(1000):
        for i in range(pos.shape[0]):
            mask = np.arange(pos.shape[0]) != i
            others = pos[mask]
            vel[i] += np.sign(others - pos[i]).sum(axis=0)
        pos += vel
    return (np.absolute(vel).sum(axis=1) * np.absolute(pos).sum(axis=1)).sum()

def repeat_individual(posD, velD):
    posD = posD.copy()
    velD = velD.copy()
    historical = set()
    iterations = 0
    while True:
        for i in range(posD.shape[0]):
            mask = np.arange(posD.shape[0]) != i
            others = posD[mask]
            velD[i] += np.sign(others - posD[i]).sum(axis=0)
        posD += velD

        mark = hash(np.append(posD, velD).tostring())
        if mark in historical:
            break
        historical.add(mark)
        iterations += 1
    return iterations

if __name__ == "__main__":
    arr = clean_input()

    pos, vel = get_posvel(arr)

    print(f"First star answer: {first_star(pos, vel)}")
    
    r0 = repeat_individual(pos[:,0], vel[:,0])
    r1 = repeat_individual(pos[:,1], vel[:,1])
    r2 = repeat_individual(pos[:,2], vel[:,2])

    print(f"Second star answer: {lcm(r0,lcm(r1,r2))}")
