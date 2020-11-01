import timeit
import numpy as np
import random

if __name__=="__main__":
    print("Arbitrary Performance Analysis for comparison.\nThis test is not strictly accurate, just use this to calculate the approximate speed compared to contest device.")

    a = 0
    t_ = timeit.default_timer()
    for i in range(1000000):
        a += 1
    print("For loop 1000000 times %fs"%(timeit.default_timer() - t_))

    l = list(range(200000))
    t_ = timeit.default_timer()
    random.shuffle(l)
    list.sort(l)
    print("Shuffle and sort 200000 Elements %fs"%(timeit.default_timer() - t_))

    
    t_ = timeit.default_timer()
    for i in range(50):
        a = np.random.randn(1000,1000)
        x = np.random.randn(1000,1000)
        b = np.dot(a,x)
    print("1000 by 1000 Matrix Multiplication 50 times with generation %fs"%(timeit.default_timer() - t_))