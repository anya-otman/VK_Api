# Использование Vk API
_____
# Подготовка к запуску
В скрипте используются модули Requests и PrettyTable, поэтому перед запуском необходимо установить их через терминал:
```
pip install requests
```
```
pip install prettytable
```
# Запуск скрипта
С помощью скрипта можно получить информацию о пользователе, список его друзей, список с названиями групп и список с названиями альбомов.    
Для запуска используйте команду:    
```
python VK_API.py [OPTIONS] [USER_ID]
```
`USER_ID` - id страницы пользователя, информацию о котором вы хотите узнать    
`OPTIONS` - опциии для получения информации    
:small_orange_diamond: Список доступных опций:    
`-i`, `--info` - информация о пользователе    
`-f`, `--friends` - список друзей пользоваеля    
`-g`, `--groups` - список с названиями групп пользователя    
`-a`, `--albums` - список с названиями альбомов пользователя    
# Примеры запусков
:heavy_exclamation_mark: Для работы с Vk API после каждого запроса требуется вводить токен доступа (о том, как его получить, можно узнать в официальной документации ВК)
## №1 Информация о пользователе
```
python VK_API.py -i 53083705
```
![Image alt](https://github.com/anya-otman/VK_Api/blob/main/examples/example1.png)
## №2 Информация о пользователе с закрытым профилем
```
python VK_API.py -i 600341658
```
![Image alt](https://github.com/anya-otman/VK_Api/blob/main/examples/example2.png)
## №3 Список друзей пользователя
```
python VK_API.py -f 53083705
```
![Image alt](https://github.com/anya-otman/VK_Api/blob/main/examples/example3.png)
## №4 Список друзей пользователя с закрытым профилем
```
python VK_API.py -f 600341658
```
![Image alt](https://github.com/anya-otman/VK_Api/blob/main/examples/example4.png)
## №5 Список групп пользователя
```
python VK_API.py -g 53083705
```
![Image alt](https://github.com/anya-otman/VK_Api/blob/main/examples/example5.png)
## №6 Список альбомов пользователя
```
python VK_API.py -a 53083705
```
![Image alt](https://github.com/anya-otman/VK_Api/blob/main/examples/example6.png)
## №7 Попытка получения списка альбомов при неккоректно введенном id пользователя
```
python VK_API.py -a 5308370556
```
![Image alt](https://github.com/anya-otman/VK_Api/blob/main/examples/example7.png)
## №8 Запрос без указания ключа опции
```
python VK_API.py 53083705
```
![Image alt](https://github.com/anya-otman/VK_Api/blob/main/examples/example8.png)
## №9 Попытка запроса без подключения к Интернету
```
python VK_API.py -a 53083705
```
![Image alt](https://github.com/anya-otman/VK_Api/blob/main/examples/example9.png)
