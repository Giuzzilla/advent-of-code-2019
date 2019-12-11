#https://adventofcode.com/2019/day/5

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

def both_stars(arr, input_v):
    arr = arr[:] # Copy of arr
    pos = 0
    while arr[pos] != 99:
        dig = opcode_helper(arr[pos])
        move = dig[-1]
        if move == 0:
            pos += 1
            continue
        elif move == 3:
            arr[arr[pos + 1]] = input_v
            pos += 2
            continue
        elif move == 4:
            output = arr[arr[pos + 1]]
            pos += 2
            continue

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
    return output


if __name__ == "__main__":
    arr = clean_input()
    print(f"First star answer: {both_stars(arr, 1)}")
    print(f"Second star answer: {both_stars(arr, 5)}")
