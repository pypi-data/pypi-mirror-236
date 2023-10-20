# coding=utf-8

import json
import sys
import time
from klog.common.protobuf.klog_pb2 import Log


def get_timestamp():
    return int(time.time() * 1000)


def convert_to_pb_log(data, timestamp, _id):
    """
    convert data to KLog protobuf Log
    :param data:
    :param timestamp:
    :param _id:
    :return:
    """
    if isinstance(data, dict):
        data["__id__"] = _id
        return _convert_from_dict(data, timestamp)
    else:
        pb_log = _convert_from_other(data, timestamp)
        content = Log.Content()
        content.key = "__id__"
        content.value = _id
        pb_log.contents.append(content)
        return pb_log


def _convert_from_other(data, timestamp=None):
    pb_log = Log()
    pb_log.time = timestamp

    content = Log.Content()
    content.key = "message"
    content.value = _value_to_string(data)
    pb_log.contents.append(content)
    return pb_log


def _convert_from_dict(data, timestamp=None):
    pb_log = Log()
    pb_log.time = timestamp
    for key in data:
        content = Log.Content()
        content.key = _value_to_string(key)
        value = data[key]

        if isinstance(value, dict):
            content.value = json.dumps(value)
        else:
            content.value = _value_to_string(value)

        pb_log.contents.append(content)
    return pb_log


def _value_to_string_py2(value):
    """python2 pb允许的类型为 unicode, str(utf8)"""
    if isinstance(value, basestring):
        return value
    else:
        return str(value)


def _value_to_string_py3(value):
    """python3 pb允许的类型为str, bytes(utf8)"""
    if isinstance(value, str):
        return value
    else:
        return str(value)


if sys.version_info.major == 3:
    _value_to_string = _value_to_string_py3
else:
    _value_to_string = _value_to_string_py2

