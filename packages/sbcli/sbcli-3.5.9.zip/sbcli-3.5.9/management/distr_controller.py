# coding=utf-8
import datetime
import logging

from management.rpc_client import RPCClient

from management.kv_store import DBController

logger = logging.getLogger()


def send_node_status_event(node_id, node_status):
    db_controller = DBController()
    logging.info(f"Sending event updates, node: {node_id}, status: {node_status}")
    node_status_event = {
        "timestamp": datetime.datetime.now().isoformat("T", "seconds") + 'Z',
        "event_type": "node_status",
        "UUID_node": node_id,
        "status": node_status}
    events = {"events": [node_status_event]}
    logger.debug(node_status_event)
    snodes = db_controller.get_storage_nodes()
    for node in snodes:
        if node.status != node.STATUS_ONLINE:
            continue
        logger.info(f"Sending to: {node.get_id()}")
        rpc_client = RPCClient(node.mgmt_ip, node.rpc_port, node.rpc_username, node.rpc_password)
        ret = rpc_client.distr_status_events_update(events)


def send_dev_status_event(storage_ID, dev_status):
    db_controller = DBController()
    logging.info(f"Sending event updates, device: {storage_ID}, status: {dev_status}")
    node_status_event = {
        "timestamp": datetime.datetime.now().isoformat("T", "seconds") + 'Z',
        "event_type": "device_status",
        "storage_ID": storage_ID,
        "status": dev_status}
    events = {"events": [node_status_event]}
    logger.debug(node_status_event)
    snodes = db_controller.get_storage_nodes()
    for node in snodes:
        if node.status != node.STATUS_ONLINE:
            continue
        logger.info(f"Sending to: {node.get_id()}")
        rpc_client = RPCClient(node.mgmt_ip, node.rpc_port, node.rpc_username, node.rpc_password)
        ret = rpc_client.distr_status_events_update(events)


def disconnect_device(device):
    db_controller = DBController()
    snodes = db_controller.get_storage_nodes()
    for node in snodes:
        if node.status != node.STATUS_ONLINE:
            continue
        new_remote_devices = []
        rpc_client = RPCClient(node.mgmt_ip, node.rpc_port, node.rpc_username, node.rpc_password)
        for rem_dev in node.remote_devices:
            if rem_dev.get_id() == device.get_id():
                ctrl_name = rem_dev.remote_bdev[:-2]
                rpc_client.bdev_nvme_detach_controller(ctrl_name)
            else:
                new_remote_devices.append(rem_dev)
        node.remote_devices = new_remote_devices
        node.write_to_db(db_controller.kv_store)


def get_distr_cluster_map(snodes, target_node):
    map_cluster = {}
    map_prob = []
    for snode in snodes:
        if snode.status != snode.STATUS_ONLINE:
            logger.debug(f"Node is not online: {snode.get_id()}, status: {snode.status}")
            continue
        dev_map = {}
        dev_w_map = []
        node_w = 0

        for i, dev in enumerate(snode.nvme_devices):
            if dev.status != "online":
                logger.debug(f"Device is not online: {dev.get_id()}, status: {dev.status}")
                continue
            dev_w = int(dev.size/(1024*1024*1024)) or 1
            node_w += dev_w
            if snode.get_id() == target_node.get_id():
                name = dev.alceml_bdev
            else:
                for dev2 in target_node.remote_devices:
                    if dev2.get_id() == dev.get_id():
                        name = dev2.remote_bdev
                        break
            dev_map[dev.cluster_device_order] = {
                "UUID": dev.get_id(),
                "bdev_name": name,
                "status": "online"}
            dev_w_map.append({
                "weight": dev_w,
                "id": dev.cluster_device_order})
        map_cluster[snode.get_id()] = {
                "availability_group": 0,
                "status": "online",
                "devices": dev_map}
        map_prob.append({
            "weight": node_w,
            "items": dev_w_map
        })
    cl_map = {
        "name": "",
        "UUID_node_target": "",
        "timestamp": datetime.datetime.now().isoformat("T", "seconds")+'Z',
        "map_cluster": map_cluster,
        "map_prob": map_prob
    }
    return cl_map
