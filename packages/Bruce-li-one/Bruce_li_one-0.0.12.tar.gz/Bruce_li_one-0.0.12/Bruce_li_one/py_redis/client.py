#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/2/13 
# @Author :wsli
# @File : client.py
# @Software: PyCharm
import redis
import json
class Bruce_redis():
    def __init__(self,pool):
        self.POOL=pool
        self.redis_client=redis.Redis(connection_pool=pool)
    def get(self, key):
        """
        获取单个值
        :param key:
        :return:
        """
        value = self.redis_client.get(key)
        return value

    def mget(self, *args):
        """
        获取多个值
        :param args:
        :return:
        """
        value = self.redis_client.mget(*args)
        return value

    def set(self, key, value):
        """
        设置单个值
        :param key:
        :param value:
        :return:
        """
        value = self.redis_client.set(key, value)
        return value

    def mset(self, *args, **kwargs):
        """
        设置多个键值
        :return:
        """
        value = self.redis_client.mset(*args, **kwargs)
        return value

    def is_key_true(self, key):
        """
        判断key值是否存在
        :return:
        """
        status = self.redis_client.exists(key)
        return status

    def del_key(self, key):
        """
        删除key
        :param key:
        :return:
        """
        status = self.redis_client.delete(key)
        return status

    def clear_db_data(self):
        """
        清除当前数据库中所有数据
        :return:
        """
        pass

    def clear_dball_data(self):
        """
        清除所有库中所有数据
        :return:
        """
        pass

    def set_json(self, keyName, jsonstr):
        """
        存入json到redis中
        :return:
        """
        jsonstr = json.dumps(jsonstr)
        status=self.redis_client.set(keyName, jsonstr)
        return status

    def get_json(self, keyName):
        """
        获取key的json值
        :param keyName:
        :return:
        """

        val = self.get(keyName)
        return json.loads(val)

    def close(self):
        self.POOL.release(self.redis_client)

class Bruce_redis_pool:
    def __init__(self,host="localhost",port=6379,password="",db=0,decode_responses=True,max_connections=10):
        #创建连接池
        self.pool = redis.ConnectionPool(host=host, port=port, password=password,db=db,decode_responses=decode_responses,max_connections=max_connections)

    def get_cont_idle(self):
        """
        获取连接池空闲
        """
        pass

    def get_cont_active(self):
        """
        获取连接池活跃
        """
        pass

    def create_redis_client(self):
        """
        连接池中拿一个连接
        """
        # 获取Redis连接
        conn = Bruce_redis(self.pool)
        return conn

    def pool_close(self):
        self.pool.close()



# CC=Bruce_redis_pool(password="pt126888")
# BB=CC.create_redis_client()
# BB.set('TEST','123')
# BB.close()
# BB.set('TEST123','12132133')


# import redis
# # 建立连接池
# pool = redis.ConnectionPool(host='localhost', port=6379, db=0,password="pt126888")
# # 获取连接对象
# r = redis.Redis(connection_pool=pool)
# # 接下来可以使用r连接对象进行跟Redis的各种操作
# r.set('foo', 'bar')
# value = r.get('foo')
# print(value)
# # 操作完成后将连接对象归还回连接池
# pool.release(r)