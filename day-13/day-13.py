#https://adventofcode.com/2019/day/13
import numpy as np

def clean_input(path = "./day-13/input.txt"):
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
    if star == 2:
        arr[0] = 2
    arr.extend([0]*10000)
    block_count = 0
    terminated = False
    pos = 0
    relativeBase = 0
    joystick = 0
    paddle_pos_x = False
    ball_pos_x = False
    while not terminated:
        out1, arr, pos, terminated, relativeBase = reader(arr, joystick, pos=pos, relativeBase=relativeBase)
        out2, arr, pos, terminated, relativeBase = reader(arr, joystick, pos=pos, relativeBase=relativeBase)
        out3, arr, pos, terminated, relativeBase = reader(arr, joystick, pos=pos, relativeBase=relativeBase)
        
        if out3 == 2:
            block_count += 1
        elif out3 == 3:
            paddle_pos_x = out1
        elif out3 == 4:
            ball_pos_x = out1

        if paddle_pos_x and ball_pos_x:
            joystick = np.sign(ball_pos_x - paddle_pos_x)

        if out1 == -1 and out2 == 0:
            last_out = out3

    if star == 1:
        return block_count
    elif star == 2:
        return last_out

if __name__ == "__main__":
    arr = clean_input()
    print(f"First star answer: {both_stars(arr, 1)}")
    print(f"Second star answer: {both_stars(arr, 2)}")
