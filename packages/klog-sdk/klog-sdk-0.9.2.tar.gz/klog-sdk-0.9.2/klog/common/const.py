X_KLOG_API_VERSION = "py0.9.2"

MAX_KEY_COUNT = 900  # amount
MAX_KEY_SIZE = 1 << 20  # byte
MAX_VALUE_SIZE = 1 << 20  # byte
MAX_BULK_SIZE = 4096  # amount
MAX_LOG_SIZE = 3000000  # byte
MAX_LOG_GROUP_SIZE = 3000000  # byte

MAX_RETRIES = 10000

ERR_MAX_KEY_COUNT = "KeyCountError(max={})".format(MAX_KEY_COUNT)
ERR_MAX_KEY_SIZE = "KeySizeError(max={}bytes)".format(MAX_KEY_SIZE)
ERR_MAX_VALUE_SIZE = "ValueSizeError(max={}bytes)".format(MAX_VALUE_SIZE)
ERR_MAX_LOG_SIZE = "LogSizeError(max={}bytes)".format(MAX_LOG_SIZE)

SERVICE_NAME = 'klog'
DEFAULT_REGION = 'inner'
DEFAULT_API_ENDPOINT = 'klog.api.ksyun.com'
API_VERSION = "2020-07-31"

TIME_UNIT = ['s', 'm', 'h', 'd', 'w', 'M']

DEFAULT_KLOG_REGION_BEIJING = "cn-beijing-6"
