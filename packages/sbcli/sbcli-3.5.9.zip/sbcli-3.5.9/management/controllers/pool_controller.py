# coding=utf-8

import logging as lg

import json
import random
import string
import uuid

from management import utils
from management.kv_store import DBController
from management.models.device_stat import LVolStat
from management.models.pool import Pool

logger = lg.getLogger()

db_controller = DBController()


def _generate_string(length):
    return ''.join(random.SystemRandom().choice(
        string.ascii_letters + string.digits) for _ in range(length))


def add_pool(name, pool_max, lvol_max, max_rw_iops, max_rw_mbytes, max_r_mbytes, max_w_mbytes, has_secret):
    logger.info("Adding pool")
    pool = Pool()
    pool.id = str(uuid.uuid4())
    pool.pool_name = name
    if has_secret:
        pool.secret = _generate_string(20)
    pool.pool_max_size = pool_max or 0
    pool.lvol_max_size = lvol_max or 0
    pool.max_rw_ios_per_sec = max_rw_iops or 0
    pool.max_rw_mbytes_per_sec = max_rw_mbytes or 0
    pool.max_r_mbytes_per_sec = max_r_mbytes or 0
    pool.max_w_mbytes_per_sec = max_w_mbytes or 0
    pool.status = "active"
    pool.write_to_db(db_controller.kv_store)
    logger.info("Done")
    return name


def set_pool_value_if_above(pool, key, value):
    logger.info(f"Updating pool {key}: {value}")
    current_value = getattr(pool, key)
    if value > current_value:
        setattr(pool, key, value)
        return True
    else:
        logger.error(f"{key}: {value} can't be less than current value: {current_value}")
        return False


def set_pool(uuid, pool_max, lvol_max, max_rw_iops,
             max_rw_mbytes, max_r_mbytes, max_w_mbytes):
    pool = db_controller.get_pool_by_id(uuid)
    if not pool:
        logger.error(f"Pool not found {uuid}")
        return False

    if pool.status == Pool.STATUS_INACTIVE:
        logger.error("Pool is disabled")
        return False

    if pool_max:
        if not set_pool_value_if_above(pool, "pool_max_size", pool_max):
            return False
    if lvol_max:
        if not set_pool_value_if_above(pool, "lvol_max_size", lvol_max):
            return False

    if max_rw_iops:
        if not set_pool_value_if_above(pool, "max_rw_ios_per_sec", max_rw_iops):
            return False
    if max_rw_mbytes:
        if not set_pool_value_if_above(pool, "max_rw_mbytes_per_sec", max_rw_mbytes):
            return False
    if max_r_mbytes:
        if not set_pool_value_if_above(pool, "max_r_mbytes_per_sec", max_r_mbytes):
            return False
    if max_w_mbytes:
        if not set_pool_value_if_above(pool, "max_w_mbytes_per_sec", max_w_mbytes):
            return False

    pool.write_to_db(db_controller.kv_store)
    logger.info("Done")
    return True


def delete_pool(uuid):
    pool = db_controller.get_pool_by_id(uuid)
    if not pool:
        logger.error(f"Pool not found {uuid}")
        return False
    if pool.status == Pool.STATUS_INACTIVE:
        logger.error(f"Pool is disabled")
        return False

    if pool.lvols:
        logger.error(f"Pool is not empty {uuid}")
        return False

    logger.info(f"Deleting pool {pool.id}")
    pool.remove(db_controller.kv_store)
    logger.info("Done")
    return True


def list_pools(is_json):
    pools = db_controller.get_pools()
    data = []
    for pool in pools:
        data.append({
            "UUID": pool.id,
            "Name": pool.pool_name,
            "Capacity": utils.humanbytes(get_pool_total_capacity(pool.get_id())),
            "Max size": utils.humanbytes(pool.pool_max_size),
            "LVol Max Size": utils.humanbytes(pool.lvol_max_size),
            "LVols": f"{len(pool.lvols)}",
            "QOS": f"{pool.has_qos()}",
            "Status": pool.status,
        })

    if is_json:
        return json.dumps(data, indent=2)
    else:
        return utils.print_table(data)


def add_lvol(lvol_id, pool_id):
    lvol = db_controller.get_lvol_by_id(lvol_id)
    if not lvol:
        logger.error("lvol not found")
        return False

    pool = db_controller.get_pool_by_id(pool_id)
    if not pool:
        logger.error("pool not found")
        return False
    logger.info(f"Adding lvol:{lvol_id} to pool:{pool_id}")
    lvol.pool_uuid = pool.id
    lvol.write_to_db(db_controller.kv_store)
    if lvol_id not in pool.lvols:
        pool.lvols.append(lvol_id)
        pool.write_to_db(db_controller.kv_store)
    logger.info("Done")
    return True


def delete_lvol(lvol_id, pool_id):
    pool = db_controller.get_pool_by_id(pool_id)
    logger.info(f"Removing lvol:{lvol_id} from pool:{pool_id}")
    if not pool:
        logger.error(f"Pool not found {pool_id}")
        return False

    if lvol_id in pool.lvols:
        pool.lvols.remove(lvol_id)
    pool.write_to_db(db_controller.kv_store)

    lvol = db_controller.get_lvol_by_id(lvol_id)
    if not lvol:
        logger.error("lvol not found")
        return False
    lvol.pool_uuid = ''
    lvol.write_to_db(db_controller.kv_store)
    logger.info("Done")
    return True


def set_status(pool_id, status):
    pool = db_controller.get_pool_by_id(pool_id)
    logger.info(f"Setting pool:{pool_id} status to Active")
    if not pool:
        logger.error(f"Pool not found {pool_id}")
        return False
    pool.status = status
    pool.write_to_db(db_controller.kv_store)
    logger.info("Done")


def get_pool(pool_id, is_json):
    pool = db_controller.get_pool_by_id(pool_id)
    if not pool:
        logger.error(f"Pool not found {pool_id}")
        return False

    data = pool.get_clean_dict()
    if is_json:
        return json.dumps(data, indent=2)
    else:
        data2 = [{"key": key, "value": data[key]} for key in data]
        return utils.print_table(data2)


def get_capacity(pool_id):
    pool = db_controller.get_pool_by_id(pool_id)
    if not pool:
        logger.error(f"Pool not found {pool_id}")
        return False

    out = []
    total_size = 0
    for lvol_id in pool.lvols:
        lvol = db_controller.get_lvol_by_id(lvol_id)
        total_size += lvol.size
        out.append({
            "LVol name": lvol.lvol_name,
            "provisioned": utils.humanbytes(lvol.size),
            "util_percent": 0,
            "util": 0,
        })
    if pool.lvols:
        out.append({
            "device name": "Total",
            "provisioned": utils.humanbytes(total_size),
            "util_percent": 0,
            "util": 0,
        })
    return utils.print_table(out)


def get_io_stats(pool_id):
    pool = db_controller.get_pool_by_id(pool_id)
    if not pool:
        logger.error(f"Pool not found {pool_id}")
        return False

    out = []
    total_values = {
        "read_bytes_per_sec": 0,
        "read_iops": 0,
        "write_bytes_per_sec": 0,
        "write_iops": 0,
        "unmapped_bytes_per_sec": 0,
        "read_latency_ticks": 0,
        "write_latency_ticks": 0,
    }
    for lvol_id in pool.lvols:
        lvol = db_controller.get_lvol_by_id(lvol_id)
        record = LVolStat(data={"uuid": lvol.get_id(), "node_id": lvol.node_id}).get_last(db_controller.kv_store)
        if not record:
            continue
        out.append({
            "LVol name": lvol.lvol_name,
            "bytes_read (MB/s)": record.read_bytes_per_sec,
            "num_read_ops (IOPS)": record.read_iops,
            "bytes_write (MB/s)": record.write_bytes_per_sec,
            "num_write_ops (IOPS)": record.write_iops,
            "bytes_unmapped (MB/s)": record.unmapped_bytes_per_sec,
            "read_latency_ticks": record.read_latency_ticks,
            "write_latency_ticks": record.write_latency_ticks,
        })
        total_values["read_bytes_per_sec"] += record.read_bytes_per_sec
        total_values["read_iops"] += record.read_iops
        total_values["write_bytes_per_sec"] += record.write_bytes_per_sec
        total_values["write_iops"] += record.write_iops
        total_values["unmapped_bytes_per_sec"] += record.unmapped_bytes_per_sec
        total_values["read_latency_ticks"] += record.read_latency_ticks
        total_values["write_latency_ticks"] += record.write_latency_ticks

    out.append({
        "LVol name": "Total",
        "bytes_read (MB/s)": total_values['read_bytes_per_sec'],
        "num_read_ops (IOPS)": total_values["read_iops"],
        "bytes_write (MB/s)": total_values["write_bytes_per_sec"],
        "num_write_ops (IOPS)": total_values["write_iops"],
        "bytes_unmapped (MB/s)": total_values["unmapped_bytes_per_sec"],
        "read_latency_ticks": total_values["read_latency_ticks"],
        "write_latency_ticks": total_values["write_latency_ticks"],
    })

    return utils.print_table(out)


def get_secret(pool_id):
    pool = db_controller.get_pool_by_id(pool_id)
    if not pool:
        logger.error(f"Pool not found {pool_id}")
        return False

    if pool.secret:
        return pool.secret
    else:
        return "Pool has no secret"


def set_secret(pool_id, secret):
    pool = db_controller.get_pool_by_id(pool_id)
    if not pool:
        logger.error(f"Pool not found {pool_id}")
        return False

    secret = secret.strip()
    if len(secret) < 20:
        return "Secret must be at least 20 char"

    pool.secret = secret
    pool.write_to_db(db_controller.kv_store)


def get_pool_total_capacity(pool_id):
    pool = db_controller.get_pool_by_id(pool_id)
    if not pool:
        logger.error(f"Pool not found {pool_id}")
        return False
    total = 0
    for lvol_id in pool.lvols:
        lvol = db_controller.get_lvol_by_id(lvol_id)
        total += lvol.size

    snaps = db_controller.get_snapshots()
    for snap in snaps:
        if snap.lvol.pool_uuid == pool_id:
            total += snap.lvol.size
    return total


def get_pool_total_rw_iops(pool_id):
    pool = db_controller.get_pool_by_id(pool_id)
    if not pool:
        logger.error(f"Pool not found {pool_id}")
        return False
    if pool.max_rw_ios_per_sec <= 0:
        return 0

    total = 0
    for lvol_id in pool.lvols:
        lvol = db_controller.get_lvol_by_id(lvol_id)
        total += lvol.rw_ios_per_sec

    return total


def get_pool_total_rw_mbytes(pool_id):
    pool = db_controller.get_pool_by_id(pool_id)
    if not pool:
        logger.error(f"Pool not found {pool_id}")
        return False
    if pool.max_rw_mbytes_per_sec <= 0:
        return 0

    total = 0
    for lvol_id in pool.lvols:
        lvol = db_controller.get_lvol_by_id(lvol_id)
        total += lvol.rw_mbytes_per_sec

    return total


def get_pool_total_r_mbytes(pool_id):
    pool = db_controller.get_pool_by_id(pool_id)
    if not pool:
        logger.error(f"Pool not found {pool_id}")
        return False
    if pool.max_r_mbytes_per_sec <= 0:
        return 0

    total = 0
    for lvol_id in pool.lvols:
        lvol = db_controller.get_lvol_by_id(lvol_id)
        total += lvol.r_mbytes_per_sec

    return total


def get_pool_total_w_mbytes(pool_id):
    pool = db_controller.get_pool_by_id(pool_id)
    if not pool:
        logger.error(f"Pool not found {pool_id}")
        return False
    if pool.max_w_mbytes_per_sec <= 0:
        return 0

    total = 0
    for lvol_id in pool.lvols:
        lvol = db_controller.get_lvol_by_id(lvol_id)
        total += lvol.w_mbytes_per_sec

    return total
