# coding=utf-8
import time
import threading

from klog.common.exception.exceptions import KLogException
from klog.common.k_logger import logger
from klog.common.rate_limit import RateLimit
from klog.cli.sender import Sender
from klog.common.snowflake import generator


class Worker:
    def __init__(self, queue,
                 endpoint,
                 credential,
                 rate_limit,
                 max_retries,
                 retry_interval,
                 machine_id,
                 **kwargs):

        self.queue = queue
        self.endpoint = endpoint
        self.credential = credential
        self.max_retries = max_retries
        self.retry_interval = retry_interval

        self.id_generator = generator(machine_id)

        if rate_limit > 0:
            self.rate_limit = RateLimit(limit_per_sec=rate_limit)
        else:
            self.rate_limit = None

        self.senders = dict()

        self.flush_event = threading.Event()
        self.flush_done_event = threading.Event()

        self.kwargs = kwargs
        self.check_env()

    def flush(self, timeout=10):
        logger.debug("Worker.flush: got flush signal, timeout=%s", timeout)
        self.flush_event.set()
        self.flush_done_event.wait(timeout)
        self.flush_event.clear()
        self.flush_done_event.clear()

    def run(self):
        last_checked_at = time.time()
        while True:
            item = self.queue.get(block=True, timeout=0.1)

            # buffer满，发送
            if item:
                if self.rate_limit:
                    self.rate_limit.wait()
                item.id = str(next(self.id_generator))
                sender = self.get_sender(item.project_name, item.log_pool_name, item.source, item.filename)
                sender.add_data(item)
                if sender.buffer_full():
                    sender.send()

            # 超过一定时间间隔，发送
            now = time.time()
            if now - last_checked_at > 0.1:
                last_checked_at = now
                for sender in self.senders.values():
                    if now - sender.get_last_send_time() > 2:
                        sender.send()

            # 收到flush信号，发送
            if self.flush_event.is_set() and self.queue.size() == 0:
                logger.debug("KLog.Worker.run: got flush signal and queue is empty")
                for sender in self.senders.values():
                    sender.send()
                self.flush_done_event.set()

    def get_sender(self, project_name, log_pool_name, source, filename):
        # 使用KLog sender
        key = "{}__{}__{}__{}".format(project_name, log_pool_name, source, filename)
        sender = self.senders.get(key)
        if not sender:
            sender = Sender(self.endpoint,
                            self.credential,
                            project_name,
                            log_pool_name,
                            source,
                            filename,
                            self.max_retries,
                            self.retry_interval)
            self.senders[key] = sender
        return sender

    def check_env(self):
        if self.credential is None or not self.credential.secret_id or not self.credential.secret_key:
            raise KLogException("NoCredentialException", "please set credential or access_key and secret_key")
