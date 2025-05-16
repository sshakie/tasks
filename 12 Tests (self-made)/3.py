from yandex_testing_lesson import strip_punctuation_ru


# !()—[]{};:'"\,<>./?@#$%^&*_~


def test_strip_punctuation_ru():
    test_data = (('ах, да!', 'ах да'),
                 ('не будет...', 'не будет'),
                 ('Кое-какие мечты', 'Кое-какие мечты'),
                 ('ого:;",<>()[]{}', 'ого'),
                 ('', ''),
                 ('да! да?" нет.', 'да да нет'),
                 ("да—нет'хе", "да нет хе"),
                 ('капуста, дижнсы/ как он хо@тел', 'капуста дижнсы как он хо тел'),
                 ('борода#как$у%него ^если&он**хотел_то~ушел бы', 'борода как у него если он хотел то ушел бы'),
                 ('замок\\исчезающей девы', 'замок исчезающей девы'))

    for my_data, correct_data in test_data:
        try:
            result = strip_punctuation_ru(my_data)
        except Exception:
            print('NO')
            return False
        else:
            if result != correct_data:
                print('NO')
                return False
    print('YES')
    return True


test_strip_punctuation_ru()
