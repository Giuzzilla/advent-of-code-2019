#%%

def clean_input(path = "/home/giuzzilla/Desktop/advent-of-code-2019/day-8/input.txt"):
    input_f = open(path).readlines()
    return [int(el) for el in input_f[0].strip()]

def first_star(arr, shape):
    from collections import Counter

    counts = []
    size = shape[0] * shape[1]
    for i in range(len(arr) // size):
        count = Counter(arr[i*size:(i+1)*(size)])
        counts.append(count)
    
    min_0 = min(counts, key=lambda d: d[0])

    return min_0[1] * min_0[2]

def second_star(arr, shape, writepath = './solution-star2.png'):
    import cv2
    import numpy as np
    from functools import reduce

    vectors = []
    size = shape[0] * shape[1]
    for i in range(len(arr) // size):
        vectors.append(np.array(arr[i*size:(i+1)*(size)]))
    
    vect_f = np.frompyfunc(lambda x,y: x if x != 2 else y, 2, 1)
        
    final = reduce(vect_f, vectors).astype('int32')
    cv2.imwrite(writepath, 255*final.reshape(shape))

    return "Written to " + writepath

if __name__ == "__main__":
    arr = clean_input()
    shape = (6, 25)

    print(f"First star answer: {first_star(arr, shape)}")
    print(f"Second star answer: {second_star(arr, shape)}")
