list = [1, -2, 3, 6, -4, -7]


def hello(list):
    counter = 0
    for _ in list:
        if _ < 0:
            counter += 1

    return counter


result = hello(list)
print(result)
