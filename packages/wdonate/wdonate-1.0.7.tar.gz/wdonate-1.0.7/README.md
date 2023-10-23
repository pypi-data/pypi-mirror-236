#Как пользоваться библиотекой?

Сайт: wdonate.ru
Автор питон библы: vk.com/id486001202

Сначало инициализируем класс:

from wdonate.wdonate import wdonate
wd = wdonate('токен wdonate', group_id)

Методы к котором вы можете далее обратиться:

wd.getBalance() -> float - получение баланса

wd.getLink(user_id: int, amount: float = 0, payload: int = 0, pay_method: str = 'card') -> dict 
Получение ссылки для оплаты

wd.getPayments(count: int = 0) -> dict - получение списка последних донатов

wd.getCallback() -> dict - получение текущей url callback

wd.setCallback(url: str) -> dict - установка url callback

wd.delCallback() -> dict - удаление текущей url callback
