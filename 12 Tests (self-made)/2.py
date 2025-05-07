def is_correct_mobile_phone_number_ru(number):
    if not number.startswith('8') and not number.startswith('+7'):
        return False

    true_number = []
    for i, ii in enumerate(number):
        if ii.isdigit():
            true_number.append(ii)
        elif i == 0 and ii == '+':
            continue
        elif ii not in [' ', '-', '(', ')']:
            return False
    if len(true_number) != 11:
        return False

    if '(' in number or ')' in number:
        if number.count('(') != 1 or number.count(')') != 1:
            return False
        if number.index(')') <= number.index('('):
            return False

        check = number[number.index('(') + 1:number.index(')')]
        if len(check) != 3 or not check.isdigit():
            return False
    return True


if is_correct_mobile_phone_number_ru(input()):
    print('YES')
else:
    print('NO')
