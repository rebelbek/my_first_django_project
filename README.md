# Проект py_dd

В проекте содержится приложение stocks, которое получает
данные с мосбиржи, сохраняет их в базу данных и отображает в html.

## Настройка

Создайте файл **.env** в папке **env** которая находится в корне проекта
**py_dd** и добавьте следующие настройки:

```
url_stocks = https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.xml
url_stock = https://iss.moex.com/iss/engines/stock/markets/shares/boards/{BOARDID}/securities/{TICKER}.xml
```

## Запуск

