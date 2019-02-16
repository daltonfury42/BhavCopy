import redis

from bhavcopy import model


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

    def get_equity_by_name_date(self, name, date):

        key = 'equity:' + name + ':' + date.strftime('%d%m%y')

        hashval = self.db.hgetall(key)

        return model.Equity(code=int(hashval['code']),
                            name=hashval['name'],
                            open=float(hashval['open']),
                            high=float(hashval['high']),
                            low=float(hashval['low']),
                            close=float(hashval['close']))
