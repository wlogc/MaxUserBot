# MaxUserBot

Простой юзер-бот для пересылки сообщений между чатом в «Максе» и Telegram-чатом.  
Работает на Python 3.9+, требует только двух pip-пакетов.
Делал его давно только щас решил залить!
---

## Установка

1. Склонируй репозиторий  
   git clone https://github.com/wlogc/MaxUserBot.git  
   cd MaxUserBot  

2. Установи зависимости  
   pip install -r requirements.txt  

3. Заполни config.py (пример ниже)

---

## Настройка

Все настройки хранятся в файле config.py:

BOT_TOKEN   = "1"             # токен ТГ-бота  
TG_SEND_ID  = 123             # ID Telegram-чата куда пересылаем  
MAX_CHAT_ID = -123456778      # ID чата в «Максе» откуда берём  
MAX_TOKEN   = "max token here"  # токен авторизации из localStorage Макса  

Как получить MAX_TOKEN:  
1. Открой браузерную версию Макса  
2. F12 → Console  
3. Вставь и нажми Enter:  
   console.log(JSON.parse(localStorage.getItem('__oneme_auth')));  
4. Скопируй значение поля token в MAX_TOKEN

---

## Команды бота (вводятся в любом чате, где есть бот)

.ping        — отвечает PONG и удаляет команду  
.calc 2+2    — считает выражение Python и выводит результат  
.run print(1) — выполняет произвольный Python-код (осторожно!)  
.setMax      — запоминает ТЕКУЩИЙ чат Макса как источник пересылки  
.setTg 987654 — запоминает указанный Telegram-чат как приёмник  

Команды автоматически удаляются после выполнения.

---

## Запуск

python main.py

