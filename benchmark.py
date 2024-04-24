from timeit import default_timer as timer


cycles = 1000

sum_time = 0
for i in range(cycles):
    start = timer()
    for i in range(100):
        ...

    length = timer() - start
    sum_time += length

sum_time /= cycles
print(sum_time)




