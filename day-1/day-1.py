#https://adventofcode.com/2019/day/1

def clean_input(path = "./input.txt"):
    input_f = open(path).readlines()
    return [int(item.strip()) for item in input_f]

def first_star(arr):
    return sum(map(lambda m: m // 3 - 2, arr))

def second_star(arr):
    def calculate_fuel(mass):
        current_fuel = mass // 3 - 2
        total_fuel = 0
        while current_fuel > 0:
            total_fuel += current_fuel
            current_fuel = current_fuel // 3 - 2
        return total_fuel

    return sum(map(calculate_fuel, arr))

if __name__ == "__main__":
    orig = clean_input()
    print(f"First answer: {first_star(orig)}")
    print(f"Second answer: {second_star(orig)}")

