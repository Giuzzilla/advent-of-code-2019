#https://adventofcode.com/2019/day/2

def clean_input(path = "./input.txt"):
    input_f = open(path).readlines()
    return [int(el) for el in input_f[0].strip().split(',')]

def first_star(arr, new_pos1, new_pos2):
    arr = arr[:] # Copy of arr
    arr[1] = new_pos1
    arr[2] = new_pos2
    pos = 0
    while arr[pos] != 99:
        if arr[pos] == 1:
            arr[arr[pos + 3]] = arr[arr[pos + 1]] + arr[arr[pos + 2]]
        elif arr[pos] == 2:
            arr[arr[pos + 3]] = arr[arr[pos + 1]] * arr[arr[pos + 2]]
        pos += 4
    return arr[0]

def second_star(arr, required):
    for i in range(0, 99):
        for j in range(0, 99):
            if first_star(arr, i, j) == required:
                return i*100 + j

if __name__ == "__main__":
    arr = clean_input()
    print(f"First star answer: {first_star(arr, 12, 2)}")
    print(f"Second star answer: {second_star(arr, 19690720)}")

