# Как пользоваться библиотекой?

Сайт: wdonate.ru
Автор питон библы: vk.com/id486001202

Для установки:
```
pip install wdonate
```

Сначало инициализируем класс:

```python
from wdonate import wdonate
wd = wdonate('токен wdonate', group_id)
```

Методы к котором вы можете далее обратиться:

```python
wd.getBalance() -> float - получение баланса
```

Получение ссылки для оплаты:
```python
wd.getLink(user_id: int, amount: float = 0, payload: int = 0, pay_method: str = 'card') -> dict
```

получение списка последних донатов:
```python
wd.getPayments(count: int = 0) -> dict
```

получение текущей url callback:
```python
wd.getCallback() -> dict
```

установка url callback:
```python
wd.setCallback(url: str) -> dict
```

удаление текущей url callbac
```python
wd.delCallback() -> dict
```
