import time
import logging


log = logging.getLogger(__name__)


# 2010-11-4 9:42:54
epoch = 1288834974657

worker_id_bits = 10
max_worker_id = -1 ^ (-1 << worker_id_bits)
sequence_bits = 12
worker_id_shift = sequence_bits
timestamp_left_shift = sequence_bits + worker_id_bits
sequence_mask = -1 ^ (-1 << sequence_bits)


def snowflake_to_timestamp(_id):
    _id = _id >> 22   # strip the lower 22 bits
    _id += epoch    # adjust for twitter epoch
    _id = _id / 1000  # convert from milliseconds to seconds
    return _id


def generator(worker_id, sleep=lambda x: time.sleep(x/1000.0)):
    assert worker_id >= 0 and worker_id <= max_worker_id

    last_timestamp = -1
    sequence = 0

    while True:
        timestamp = int(time.time()*1000)

        if last_timestamp > timestamp:
            log.warning(
                "clock is moving backwards. waiting until %i" % last_timestamp)
            sleep(last_timestamp-timestamp)
            continue

        if last_timestamp == timestamp:
            sequence = (sequence + 1) & sequence_mask
            if sequence == 0:
                log.warning("sequence overrun")
                sequence = -1 & sequence_mask
                sleep(1)
                continue
        else:
            sequence = 0

        last_timestamp = timestamp

        yield (
                ((timestamp - epoch) << timestamp_left_shift) |
                (worker_id << worker_id_shift) |
                sequence)
