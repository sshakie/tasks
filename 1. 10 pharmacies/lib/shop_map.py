import pygame, requests, sys, os


def show_map(ll_spn=None, params=None):
    if ll_spn:
        map_request = f'http://static-maps.yandex.ru/1.x/?{ll_spn}&l=map'
    else:
        map_request = f'http://static-maps.yandex.ru/1.x/?l=map'

    if params:
        map_request += '&pt='
        map_request += '~'.join([i for i in params])
    response = requests.get(map_request)

    if not response:
        print(f'''Ошибка выполнения запроса: {map_request}
        Http статус: {response.status_code}, {response.reason}''')
        sys.exit(1)

    map_file = 'map.png'
    try:
        with open(map_file, 'wb') as file:
            file.write(response.content)
    except IOError as ex:
        print(f'Ошибка записи временного файла: {ex}')
        sys.exit(2)

    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    os.remove(map_file)
