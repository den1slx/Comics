## Публикация комиксов

Скачиваем случайную страничку [комикса](https://xkcd.com/) (картинку) и публикуем в ВК.

### Как установить

Склонируйте репозиторий.

Установите зависимости
```commandline
pip install -r requirements.txt
```

Создайте файл `.env` в корне проекта и добавьте необходимые переменные окружения:  
VK_ACCESS_TOKEN - ваш [ВК](https://vk.com/) токен с разрешениями: **scope=groups,photos,offline,wall**  
VK_GROUP_ID - id группы или id пользователя  
Note: 
* id_группы начинается с '-'. Пример: -123456789

VK_GROUP_ID также можно передать в качестве аргумента 


### Использование
Переходим в папку с репозиторием.  
Получаем подсказку:
```commandline
python main.py -h
```
Запускаем скрипт без аргументов предварительно передав их в `.env`:
```commandline
python main.py
```
или запускаем с аргументами
```commandline
python main.py -id вашid
```

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
