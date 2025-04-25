import vk_api


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
    upload = vk_api.VkUpload(vk_session)
    photo = upload.photo_wall(['static/img/Picture1.jpg', 'static/img/Picture2.jpg', 'static/img/Picture3.jpg'])

    vk1 = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
    vk2 = f"photo{photo[1]['owner_id']}_{photo[1]['id']}"
    vk3 = f"photo{photo[2]['owner_id']}_{photo[2]['id']}"
    vk = vk_session.get_api()
    vk.wall.post(attachments=[vk1, vk2, vk3])


if __name__ == '__main__':
    main()
