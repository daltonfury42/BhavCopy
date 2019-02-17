from datetime import datetime

import redis

from bhavcopy import model


class RedisDataNotFoundException(BaseException):
    pass


class SecurityDAO:

    def __init__(self, redis_host="localhost", redis_port=6379, redis_password=""):

        self.db = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    def insert_equity(self, equity):

        key = 'equity:' + equity.name + ':' + equity.date.strftime('%d%m%y')

        self.db.hset(key, 'code', equity.code)
        self.db.hset(key, 'open', equity.open)
        self.db.hset(key, 'high', equity.high)
        self.db.hset(key, 'low', equity.low)
        self.db.hset(key, 'close', equity.close)

    def get_equities(self, name='*', date=None):
        if date is None:
            query = 'equity:' + name + ':*'
        else:
            query = 'equity:' + name + ':' + date.strftime('%d%m%y')

        keys = self.db.keys(query)

        if not keys:
            raise RedisDataNotFoundException

        equities = []

        for key in keys:
            hashval = self.db.hgetall(key)

            name, date = key.split(':')[1], datetime.strptime(key.split(':')[2], '%d%m%y')

            equity = model.Equity(code=int(hashval['code']),
                                  name=name,
                                  open=float(hashval['open']),
                                  high=float(hashval['high']),
                                  low=float(hashval['low']),
                                  close=float(hashval['close']),
                                  date=date)

            equities.append(equity)

        return equities
