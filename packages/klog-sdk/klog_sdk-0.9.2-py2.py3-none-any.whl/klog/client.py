# coding=utf-8
import logging
import random
import threading
import time

from .admin_client import KlogClient
from klog.cli.worker import Worker
from klog.common import const
from klog.common.credential import Credential
from klog.common.down_sampler import DownSampler
from klog.common.k_logger import logger
from klog.common.k_queue import KQueue
from klog.common.profile.client_profile import ClientProfile
from klog.common.profile.http_profile import HttpProfile


class Client(KlogClient):
    def __init__(self, endpoint,
                 access_key="",
                 secret_key="",
                 credential=None,
                 queue_size=2000,
                 drop_when_queue_is_full=False,
                 rate_limit=0,
                 down_sample_rate=1,
                 max_retries=-1,
                 retry_interval=-1,
                 external_logger=None,
                 logger_level=logging.WARNING,
                 machine_id=0,
                 **kwargs):
        """
        创建一个 KLog 客户端

        :param endpoint:
        您的日志项目所在地区的入口地址，该地址可以在金山云控制台日志服务的项目概览中查到。
        支持`khttp`和`https`。

        :param access_key:
        您在金山云的主账户或子账户的`ACCESS KEY ID`。

        :param secret_key:
        您在金山云的主账户或子账户的`SECRET KEY ID`。

        :param queue_size:
        客户端内部缓冲队列长度。
        默认为2000条日志。

        :param drop_when_queue_is_full:
        默认情况下，当缓冲队列满时，`client.push()`会阻塞并等待空位。
        如果设置为`True`，则不等待，直接丢弃日志。
        默认为`False`

        :param rate_limit:
        限制发送速率为每秒多少条。
        此项配置可降低CPU使用率，但会降低发送速率，在日志较多时，缓冲队列可能会满。
        默认为0，即不限制。

        :param down_sample_rate:
        降采样率。
        例如设置为0.15时，将只发送15%的日志，其余丢弃。此项配置可降低CPU使用率。
        默认为1，即发送所有日志。

        :param max_retries:
        发送失败后的重试次数，达到次数后如果仍然失败则丢弃日志。
        默认为-1，即永远重试。

        :param retry_interval:
        发送失败后的重试间隔秒数。支持浮点数。
        默认为-1，即逐步增加重试间隔(但不会超过60秒)。

        :param external_logger:
        设置客户端输出自身运行状态的日志对象。
        默认为None，即使用logging模块并打印到stdout。

        :param logger_level:
        客户端内部日志打印level。默认为logging.WARNING。

        :param machine_id:
        机器ID，取值范围[1, 1023]，用于生成日志ID。如果缺省，会随机生成一个机器ID。
        """
        logger.set_level(logger_level)
        if external_logger:
            logger.set_logger(external_logger)

        self._down_sampler = DownSampler(down_sample_rate)

        self._queue = KQueue(queue_size)
        self._drop_when_queue_is_full = drop_when_queue_is_full

        credential = credential or Credential(access_key.strip(), secret_key.strip())

        super(Client, self).__init__(credential=credential, region=const.DEFAULT_REGION, logger=logger,
                                     profile=ClientProfile(httpProfile=HttpProfile(
                                         endpoint=endpoint, keepAlive=True, reqTimeout=1000000)))

        if machine_id <= 0 or machine_id > 1023:
            machine_id = random.randint(1, 1023)

        self._worker = Worker(self._queue, endpoint.strip(), credential,
                              rate_limit, max_retries, retry_interval, machine_id, **kwargs)
        self._worker_thread = threading.Thread(target=self._worker.run)
        self._worker_thread.setDaemon(True)
        self._worker_thread.start()

    def push(self, project_name, log_pool_name, source, filename, data, timestamp=None):
        """
        异步发送一条日志
        :param project_name: 项目名称
        :param log_pool_name: 日志池名称
        :param source: 日志来源，如主机名、ip等，用于进行日志上下文查询
        :param filename: 日志文件路径，用于进行日志上下文查询
        :param timestamp: 日志时间
        :param data: 日志数据，字符串或dict类型。
        注意：
        1. 在python 2.7中，data中的所有字符串都必须为unicode或utf8编码的str类型。
        2. 在python 3 中，data中的所有字符串都必须为str或utf8编码的bytes类型。
        """
        if not self._down_sampler.ok():
            return False

        block = not self._drop_when_queue_is_full
        timestamp = int(timestamp or time.time() * 1000)
        return self._queue.put(project_name.strip(), log_pool_name.strip(), source.strip(), filename.strip(), data, timestamp, block=block)

    def flush(self, timeout=None):
        """
        将当前发送缓冲区的日志全部发送，并等待返回。

        :param timeout:
        最大等待秒数，可以是小数。
        为None时，表示阻塞到发送成功或发送结束为止。这种情况下的发送失败重试策略与Client的构造参数一致。
        """
        self._worker.flush(timeout)
