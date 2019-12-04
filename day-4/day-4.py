#https://adventofcode.com/2019/day/4
from collections import Counter

def both_stars(psw_range, n_star):
    matching = 0
    for psw in range(psw_range[0], psw_range[1]):
        exist_double = False
        increasing = int(''.join(sorted([i for i in str(psw)]))) != psw

        digits = [int(i) for i in str(psw)]
        count = Counter(digits)
        for key in count.keys():
            if n_star == 1 and count[key] >= 2:
                exist_double = True
            elif n_star == 2 and count[key] == 2:
                exist_double = True

        if increasing and exist_double:
            matching += 1

    return matching

if __name__ == "__main__":
    print(f"First star answer: {both_stars([234208, 765869], 1)}")
    print(f"Second star answer: {both_stars([234208, 765869], 2)}")
