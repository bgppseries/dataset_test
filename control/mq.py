import pika
import json
from configparser import ConfigParser
from logging import INFO
from log.logger import mylogger, set_logger

def get_config():
    config = ConfigParser()
    config.read('../setting/set.config', encoding='UTF-8')
    rmq = config['Rabbitmq']
    return rmq['username'], rmq['password'], rmq['host'], rmq['port']

class producter:
    def __init__(self):
        """
        与数据库建立连接
        """
        self.logger = mylogger(__name__, INFO)
        set_logger(self.logger)
        username, password, host, port = get_config()
        credentials = pika.PlainCredentials(username, password)  # mq用户名和密码
        # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host, port, virtual_host='test', credentials=credentials))

    def _send(self, msg):
        channel = self.connection.channel()
        # 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
        channel.exchange_declare(exchange='defalut', durable=True, exchange_type='direct')

        # 指定 routing_key。delivery_mode = 2 声明消息在队列中持久化，delivery_mod = 1 消息非持久化
        channel.basic_publish(exchange='defalut', routing_key='python-test', body=msg,
                              properties=pika.BasicProperties(delivery_mode=2))

        # enchange代表交换机，为空表示使用默认交换机，routing_key是队列名
        # 注意msg可以用json初始化
        #msg=json.dumps({'OrderId':"1000%s"%i})
        print()
        self.logger.info('[info] it is the producer send a msg')
        ##todo log[info]

    def consume(self):
        channel = self.connection.channel()
        # 创建临时队列，队列名传空字符，consumer关闭后，队列自动删除
        result = channel.queue_declare('', exclusive=True)
        # 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
        channel.exchange_declare(exchange='defalut', durable=True, exchange_type='direct')
        # 绑定exchange和队列  exchange 使我们能够确切地指定消息应该到哪个队列去
        channel.queue_bind(exchange='defalut', queue=result.method.queue, routing_key='python-test')
        print(result.method.queue)
        # 定义一个回调函数来处理消息队列中的消息，这里是打印出来
        def callback(channel, method,properties,body):
            channel.basic_ack(delivery_tag=method.delivery_tag)
            print(body.decode())

        # channel.basic_qos(prefetch_count=1)
        # 告诉rabbitmq，用callback来接受消息
        channel.basic_consume(result.method.queue, callback,
                              # 设置成 False，在调用callback函数时，未收到确认标识，消息会重回队列。True，无论调用callback成功与否，消息都被消费掉
                              auto_ack=False)
        channel.start_consuming()
        self.logger.info('[info] one consumer has handeled one msg')
    def __close(self):
        self.connection.close()


def test_send():
    print(get_config())
    mq = producter()
    mq._send("this is a testmsg")

def test_consum():
    mq=producter()
    mq.consume()


if __name__ == '__main__':
    test_consum()
