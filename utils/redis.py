"""
    @author: Jedore
    @project: knowledge_work
    @file: redis.py
    @time: 4/29/21 10:23 PM
    @desc:
"""
import pickle

import redis
from redis import Redis as _Redis

from settings import REDIS_DB_DEFAULT as DEFAULT
from settings import REDIS_DB_EXTERNAL as EXTERNAL
from settings import REDIS_DB_LABEL as LABEL
from settings import REDIS_DB_SESSION as SESSION
from settings import REDIS_HOST as HOST
from settings import REDIS_MAX_CONNECTION as MAX
from settings import REDIS_PORT as PORT


class Redis(_Redis):
    def __init__(self, name):
        self.p_session = redis.ConnectionPool(host=HOST, port=PORT, db=SESSION, max_connections=MAX)
        self.p_default = redis.ConnectionPool(host=HOST, port=PORT, db=DEFAULT, max_connections=MAX)
        self.p_label = redis.ConnectionPool(host=HOST, port=PORT, db=LABEL, max_connections=MAX)
        self.p_external = redis.ConnectionPool(host=HOST, port=PORT, db=EXTERNAL, max_connections=MAX)
        super(Redis, self).__init__(connection_pool={
            'session': self.p_session,
            'default': self.p_default,
            'label': self.p_label,
            'external': self.p_external,
        }.get(name))

    def set_pickle(self, name, value, ex=None, px=None, nx=False, xx=False):
        """
        带序列化处理的 set 方法
        :param name: 键
        :type name:str
        :param value:值
        :type value:any
        :param ex:过期时间（秒）
        :type ex:int
        :param px:过期时间（毫秒）
        :type px:int
        :param nx:如果设置为True，则只有name不存在时，当前set操作才执行
        :type nx:bool
        :param xx:如果设置为True，则只有name存在时，当前set操作才执行
        :type xx:bool
        :return:调用父类的set方法
        :rtype:
        """
        pickled_data = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        return super().set(name, pickled_data, ex, px, nx, xx)

    def get_pickle(self, name, default=None):
        """
        带序列化处理的 get 方法
        :param name:键
        :type name:str
        :param default:默认值
        :type default:any
        :return:值
        :rtype:any
        """
        pickled_data = super().get(name)

        if pickled_data is None:
            return default
        value = pickle.loads(pickled_data)
        return value
