'''
:authors: Hleb2702
:license: Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2023 Hleb2702
'''

from requests import post
from random import randint as r
from .wdonate_exception import WdonateError

class wdonate:
    def __init__(self, token: str, group_id:int):
        self.token = token
        self.group = group_id

    def getBalance(self) -> float:
        try:
            return post('https://wdonate.ru/api/getBalance', json={'token':self.token, 'botId':self.group}).json()['response']['balance']
        except:
            pass
        raise WdonateError('requests error. maybe invalid token or group_id')
        
    def getLink(self, user_id: int, amount: float = 0, payload: int = 0, pay_method: str = 'card') -> dict:
        if amount < 0 or amount > 100000:
            raise WdonateError('value error. you cannot make amount less 0 or greater 100000')
        PAY_METHOD = ["card", "qiwi", "fk", "sbp"]
        if not payload:
            payload = r(-2147483647, 2147483647)
        if payload < -2147483647 or payload > 2147483647:
            raise WdonateError('value error. payload very big or very little')
        if pay_method not in PAY_METHOD:
            raise WdonateError('value error. undefindet pay_method. you should use from this list ["card", "qiwi", "fk", "sbp"]')
        try:
            link = post('https://wdonate.ru/api/getLink', json={'priority_pay_method':pay_method, 'token':self.token, 'botId':self.group, 'payload':payload, 'sum':amount, 'userId':user_id}).json()['response']['link']
            return {'link':link, 'payload':payload}
        except:
            pass
        raise WdonateError('requests error. maybe invalid token or group_id or value invalid')
    
    def getPayments(self, count: int = 0) -> dict:
        try:
            return post('https://wdonate.ru/api/getPayments', json={'token':self.token, 'botId':self.group, 'count': count}).json()['response']
        except:
            pass
        raise WdonateError('requests error. maybe invalid token or group_id or value invalid')
    
    def getCallback(self) -> dict:
        try:
            return post('https://wdonate.ru/api/getCallback', json={'token':self.token, 'botId':self.group}).json()['response']['url']
        except:
            pass
        raise WdonateError('requests error. maybe invalid token or group_id')
        
    def setCallback(self, url: str) -> dict:
        try:
            return post('https://wdonate.ru/api/setCallback', json={'token':self.token, 'botId':self.group, 'callbackUrl':url}).json()['response']['url']
        except:
            pass
        raise WdonateError('requests error. maybe invalid token or group_id or value invalid')
        
    def delCallback(self) -> dict:
        try:
            return post('https://wdonate.ru/api/delCallback', json={'token':self.token, 'botId':self.group}).json()['response']['url']
        except:
            pass
        raise WdonateError('requests error. maybe invalid token or group_id or value invalid')
        