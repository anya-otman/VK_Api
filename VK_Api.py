import argparse
import sys
import requests
from getpass import getpass
from prettytable import PrettyTable

url_pattern = 'https://api.vk.com/method/{0}?{1}&access_token={2}&v=5.131'


def get_user_info(user_id: str, token: str):
    url = url_pattern.format(
        'users.get',
        f'user_ids={user_id}&fields=bdate,country,city,is_friend,online,status,sex',
        token
    )
    try:
        user_info = requests.get(url).json()['response'][0]
    except requests.exceptions.ConnectionError:
        sys.exit("No Internet connection")
    except KeyError:
        sys.exit("Check the correctness of the user id or token")
    print('Имя: ', user_info['first_name'])
    print('Фамилия: ', user_info['last_name'])
    if user_info['is_closed'] and not user_info['can_access_closed']:
        print('Профиль пользователя скрыт настройками приватности. Дальнейшая информация недоступна')
    else:
        if user_info['sex'] == 1:
            print('Пол: женский')
        elif user_info['sex'] == 2:
            print('Пол: мужской')
        else:
            print('Пол: не указан')

        if user_info['bdate']:
            print('Дата рождения: ', user_info['bdate'])
        else:
            print('Дата рождения: не указана')

        if user_info.get('country'):
            print('Страна: ', user_info['country']['title'])
        else:
            print('Страна: не указана')

        if user_info.get('city'):
            print('Город: ', user_info['city']['title'])
        else:
            print('Город: не указан')

        if user_info['is_friend']:
            print('Есть у Вас в друзьях')
        else:
            print('Нет у Вас в друзьях')

        if user_info['online']:
            print('Онлайн')
        else:
            print('Оффлайн')

        if user_info.get('status'):
            print('Статус: ', user_info['status'])
        else:
            print('Статус: -')


def get_user_friends(user_id: str, token: str):
    is_acc_open = can_get_access(user_id, token)
    if not is_acc_open:
        sys.exit('Профиль пользователя скрыт настройками приватности. Информация недоступна')

    url = url_pattern.format('friends.get', f'user_id={user_id}', token)
    try:
        response = requests.get(url).json()['response']
        friends = requests.get(
            url_pattern.format(
                "users.get",
                f"user_ids={response['items']}&fields=country,city,online",
                token)).json()['response']
    except requests.exceptions.ConnectionError:
        sys.exit("No Internet connection")
    except KeyError:
        sys.exit("Check the correctness of the user id or token")

    friends_data = []
    for friend_info in friends:
        name = friend_info['first_name']
        last_name = friend_info['last_name']
        country = friend_info.get('country')
        if country:
            country = country['title']
        else:
            country = 'Не указана'
        city = friend_info.get('city')
        if city:
            city = city['title']
        else:
            city = 'Не указан'
        is_online = friend_info['online']
        if is_online:
            is_online = 'Онлайн'
        else:
            is_online = 'Оффлайн'
        data = [name, last_name, country, city, is_online]
        friends_data.append(data)
    table = get_table(friends_data)
    print('Количество друзей: ', len(friends))
    print(str(table))


def can_get_access(user_id: str, token: str) -> bool:
    url = url_pattern.format('users.get', f'user_ids={user_id}', token)
    try:
        user_info = requests.get(url).json()['response'][0]
    except requests.exceptions.ConnectionError:
        sys.exit("No Internet connection")
    except KeyError:
        sys.exit("Check the correctness of the user id or token")
    if user_info['is_closed'] and not user_info['can_access_closed']:
        return False
    else:
        return True


def get_table(friends_data: list) -> PrettyTable:
    head = ['Имя', 'Фамилия', 'Страна', 'Город', 'Статус в сети']
    table = PrettyTable()
    table.field_names = head
    for data in friends_data:
        table.add_row(data)
    return table


def get_user_groups(user_id: str, token: str):
    is_acc_open = can_get_access(user_id, token)
    if not is_acc_open:
        sys.exit('Профиль пользователя скрыт настройками приватности. Информация недоступна')

    url = url_pattern.format('groups.get', f'user_id={user_id}&extended=1', token)
    try:
        response = requests.get(url).json()['response']
    except requests.exceptions.ConnectionError:
        sys.exit("No Internet connection")
    except KeyError:
        sys.exit("Check the correctness of the user id or token")

    count = response['count']
    groups = response['items']
    print('Количество групп: ', count)
    for group in groups:
        print(group['name'])


def get_user_albums(user_id: str, token: str):
    is_acc_open = can_get_access(user_id, token)
    if not is_acc_open:
        sys.exit('Профиль пользователя скрыт настройками приватности. Информация недоступна')

    url = url_pattern.format('photos.getAlbums', f'owner_id={user_id}', token)
    try:
        response = requests.get(url).json()['response']
    except requests.exceptions.ConnectionError:
        sys.exit("No Internet connection")
    except KeyError:
        sys.exit("Check the correctness of the user id or token")

    count = response['count']
    albums = response['items']
    print('Количество альбомов: ', count)
    for album in albums:
        print(album['title'])


def main():
    parser = argparse.ArgumentParser(usage="python VK_Api.py [OPTION] [USER ID]")
    parser.add_argument('-i', '--info', dest='info', action='store_true', help='Info about user')
    parser.add_argument('-f', '--friends', dest='friends', action='store_true', help='User friends list')
    parser.add_argument('-g', '--groups', dest='groups', action='store_true', help='User groups list')
    parser.add_argument('-a', '--albums', dest='albums', action='store_true', help='User albums list')
    parser.add_argument('user_id', type=str, help='User id')
    args = parser.parse_args()

    token = getpass('Enter vk access token: ')
    if not token:
        sys.exit('Token was not entered')
    try:
        if args.info:
            get_user_info(args.user_id, token)
        elif args.friends:
            get_user_friends(args.user_id, token)
        elif args.groups:
            get_user_groups(args.user_id, token)
        elif args.albums:
            get_user_albums(args.user_id, token)
        else:
            sys.exit('No options were entered')
    except Exception as e:
        sys.exit(e)


if __name__ == "__main__":
    main()
