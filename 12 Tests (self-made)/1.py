def is_prime(n):
    if not n.isdigit():
        return False
    num = int(n)
    if num <= 1:
        return False
    if num == 2:
        return True
    for divisor in range(2, int(num ** 0.5) + 1):
        if num % divisor == 0:
            return False
    return True


if is_prime(input()):
    print('YES')
else:
    print('NO')