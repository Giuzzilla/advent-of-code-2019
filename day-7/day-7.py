#https://adventofcode.com/2019/day/7
from itertools import permutations


def clean_input(path = "/home/giuzzilla/Desktop/advent-of-code-2019/day-7/input.txt"):
    input_f = open(path).readlines()
    return [int(el) for el in input_f[0].strip().split(',')]

def opcode_helper(opcode):
    digits = [int(e) for e in str(opcode).zfill(5)]
    for i in range(4):
        if not digits[i] in [0, 1]:
            isOpcode = False

    retdigits = digits[:-2]
    retdigits.extend(digits[-1:])
    return retdigits

def reader(arr, phase, input_value, pos = 0, initialized = False):
    arr = arr[:] # Copy of arr
    while arr[pos] != 99:
        dig = opcode_helper(arr[pos])
        move = dig[-1]
        if move == 0:
            pos += 1
            continue
        elif move == 3:
            if not initialized:
                arr[arr[pos + 1]] = phase
                initialized = True
            else:
                arr[arr[pos + 1]] = input_value
            pos += 2
            continue
        elif move == 4:
            output = arr[arr[pos + 1]]
            pos += 2
            return output, arr, pos, False

        s1 = pos + 1
        s2 = pos + 2
        s1m = dig[2]
        s2m = dig[1]

        if move in [1, 2, 7, 8]:
            target = pos + 3
            tpos = arr[target]

        if s1m == 0:
            v1 = arr[arr[s1]]
        else:
            v1 = arr[s1]

        if s2m == 0:
            v2 = arr[arr[s2]]
        else:
            v2 = arr[s2]

        if move == 1:
            arr[tpos] = v1 + v2
            pos += 4
        elif move == 2:
            arr[tpos] = v1 * v2
            pos += 4
        elif move == 5:
            if v1 != 0:
                pos = v2
            else:
                pos += 3
        elif move == 6:
            if v1 == 0:
                pos = v2
            else:
                pos += 3
        elif move == 7:
            if v1 < v2:
                arr[tpos] = 1
            else:
                arr[tpos] = 0
            pos += 4
        elif move == 8:
            if v1 == v2:
                arr[tpos] = 1
            else:
                arr[tpos] = 0
            pos += 4
    return False, arr, pos, True


def both_stars(arr, star):
    thrusters_out = []
    if star == 1:
        perms = permutations([0, 1, 2, 3, 4])
    elif star == 2:
        perms = permutations([5, 6, 7, 8, 9])
    else:
        raise Exception("Invalid star")

    for phase in perms:
        states = [arr, arr, arr, arr, arr]
        positions = [0, 0, 0, 0, 0]
        outputs = [None, None, None, None, None]
        initialized = False
        while True:
            for i, digit in enumerate(phase):
                if not initialized and i == 0:
                    input_t = 0
                else:
                    input_t = outputs[i - 1]

                newvalue, states[i], positions[i], terminated = reader(states[i], digit, input_t, positions[i], initialized)

                if not terminated:
                    outputs[i] = newvalue

            initialized = True

            if terminated or star == 1:
                thrusters_out.append(outputs[-1])
                break

    return max(thrusters_out)

if __name__ == "__main__":
    arr = clean_input()

    print(f"First star answer: {both_stars(arr, 1)}")
    print(f"Second star answer: {both_stars(arr, 2)}")
