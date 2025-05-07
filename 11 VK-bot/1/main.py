import vk_api, datetime


def captcha_handler(captcha):
    key = input('Enter captcha code {0}: '.format(captcha.get_url())).strip()
    return captcha.try_again(key)


def auth_handler():
    key = input('Enter authentication code: ')
    remember_device = True
    return key, remember_device


def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler,
        captcha_handler=captcha_handler)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    response = vk.friends.get(fields="bdate, city")
    a = []
    if response['items']:
        for i in response['items']:
            try:
                a.append([i['first_name'], i['last_name'], i['bdate']])
            except Exception:
                pass
    for i in sorted(a, key=lambda x: x[1]):
        print(*i)


if __name__ == '__main__':
    main()
