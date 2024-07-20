def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        if n <= 1:
            return 1 if n == 1 else 0  # I think no need to add all values that are less or equal to 0 or 1 to the cache

        if n not in cache:
            cache[n] = fibonacci(n - 1) + fibonacci(n - 2)

        return cache[n]

    return fibonacci


if __name__ == '__main__':
    fun = caching_fibonacci()

    print(fun(10))
    print(fun(15))
