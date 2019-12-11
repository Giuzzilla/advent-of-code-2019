#https://adventofcode.com/2019/day/11
import numpy as np
import cv2

def clean_input(path = "./input.txt"):
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

def reader(arr, input_value, phase = None, pos = 0, relativeBase = 0, initialized = True):
    arr = arr[:] # Copy of arr
    while arr[pos] != 99:
        pos = pos
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
                if dig[2] == 0:
                    arr[arr[pos + 1]] = input_value
                elif dig[2] == 2:
                    arr[(arr[pos +1] + relativeBase)] = input_value
                elif dig[2] == 1:
                    arr[pos + 1] = input_value
                else:
                    arr[arr[pos + 1]] = input_value
            pos += 2
            continue
        elif move == 4:
            if dig[2] == 0:
                output = arr[arr[pos + 1]]
            elif dig[2] == 2:
                output = arr[(arr[pos+1] + relativeBase)]
            elif dig[2] == 1:
                output = arr[pos + 1]
            else:
                output = arr[arr[pos + 1]]
            pos += 2
            return output, arr, pos, False, relativeBase
        elif move == 9:
            if dig[2] == 0:
                relativeBase += arr[arr[pos+1]]
            elif dig[2] == 1:
                relativeBase += arr[pos + 1]
            elif dig[2] == 2:
                relativeBase += arr[(arr[pos+1] + relativeBase)]
            pos += 2
            continue

        s1 = pos + 1
        s2 = pos + 2
        s1m = dig[2]
        s2m = dig[1]
        s3m = dig[0]

        if move in [1, 2, 7, 8]:
            target = pos + 3
            if s3m == 0:
                tpos = arr[target]
            elif s3m == 2:
                tpos = arr[target] + relativeBase

        if s1m == 0:
            v1 = arr[arr[s1]]
        elif s1m == 1:
            v1 = arr[s1]
        elif s1m == 2:
            v1 = arr[(arr[s1] + relativeBase)]

        if s2m == 0:
            v2 = arr[arr[s2]]
        elif s2m == 1:
            v2 = arr[s2]
        elif s2m == 2:
            v2 = arr[(arr[s2] + relativeBase)]

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
            arr[tpos] = int(v1 < v2)
            pos += 4
        elif move == 8:
            arr[tpos] = int(v1 == v2)
            pos += 4
    return False, arr, pos, True, relativeBase

def both_stars(arr, star):
    mat = np.zeros((1000, 1000), dtype=np.int32)

    ar = arr.copy()
    ar.extend([0]* 1000)
    current_pos = np.array((500, 500))
    pos = 0
    terminated = False
    relativeBase = 0

    # Ugly, I know. Will think of rotations later
    directions = {
        'up': np.array((-1, 0)),
        'down': np.array((1, 0)),
        'left': np.array((0, -1)),
        'right': np.array((0, 1))
    }

    def turn(num, direction):
        if num == 0:
            if direction == 'up':
                return 'left'
            elif direction == 'down':
                return 'right'
            elif direction == 'left':
                return 'down'
            elif direction == 'right':
                return 'up'
        elif num == 1:
            if direction == 'up':
                return 'right'
            elif direction == 'down':
                return 'left'
            elif direction == 'left':
                return 'up'
            elif direction == 'right':
                return 'down'

    current_direction = 'up'

    colored = []

    if star == 2:
        mat[(500,500)] = 1

    while True:
        index = tuple(current_pos)
        input1 = mat[index]
        output1, ar, pos, terminated, relativeBase = reader(ar, input1, pos = pos, relativeBase = relativeBase)

        if terminated:
            break

        mat[index] = output1
        if index not in colored:
            colored.append(index)        

        output2, ar, pos, terminated, relativeBase = reader(ar, input1, pos = pos, relativeBase = relativeBase)
        
        if terminated:
            break

        current_direction = turn(output2, current_direction)
        current_pos += directions[current_direction]

    if star == 1:
        return len(colored)
    elif star == 2:
        cv2.imwrite('./result.png', 255*mat)
        return 'Printed to results.png'

if __name__ == "__main__":
    arr = clean_input()
    print(f"First star answer: " + str(both_stars(arr, 1)))
    print(f"Second star answer: " + both_stars(arr, 2))
