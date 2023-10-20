import requests


def buscar_avatar(usuario):
    """
    Busca o avatar de um usuário no GitHub.
    :param usuario: Nome do usuário (string);
    :return: Avatar do usuário informado.
    """
    url = f'https://api.github.com/users/{usuario}'
    r = requests.get(url)
    return r.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('Zanettifabio'))
