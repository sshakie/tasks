def is_prime(n):
    if n <= 1 or not isinstance(n, int):
        return False
    for divisor in range(2, int(n ** 0.5)):
        if n % divisor == 0:
            return False
    return True


if is_prime(input()):
    print('YES')
else:
    print('NO')
