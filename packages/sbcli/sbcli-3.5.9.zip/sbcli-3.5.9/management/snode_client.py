import json

import requests
import logging

from requests.adapters import HTTPAdapter
from urllib3 import Retry

logger = logging.getLogger()


class SNodeClientException(Exception):
    def __init__(self, message):
        self.message = message


class SNodeClient:

    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.url = 'http://%s/snode/' % self.ip_address
        self.timeout = 10
        self.session = requests.session()
        self.session.verify = False
        self.session.timeout = self.timeout
        self.session.headers['Content-Type'] = "application/json"
        retries = Retry(total=30, backoff_factor=1, connect=30, read=30)
        self.session.mount("http://", HTTPAdapter(max_retries=retries))

    def _request(self, method, path, params=None):
        try:
            logger.debug("Requesting path: %s, params: %s", path, params)
            dt = None
            if params:
                dt = json.dumps(params)
            response = self.session.request(method, self.url+path, data=dt)
        except Exception as e:
            raise e

        logger.debug("Response: status_code: %s, content: %s",
                     response.status_code, response.content)
        ret_code = response.status_code

        result = None
        error = None
        if ret_code == 200:
            try:
                data = response.json()
            except Exception:
                return response.content, None

            if 'results' in data:
                result = data['results']
            if 'error' in data:
                error = data['error']
            if result is not None or error is not None:
                return result, error
            else:
                return data, None

        if ret_code in [500, 400]:
            raise SNodeClientException("Invalid http status: %s" % ret_code)
        logger.error("Unknown http status: %s", ret_code)
        return None, None

    def is_live(self):
        return self._request("GET", "")

    def info(self):
        return self._request("GET", "info")

    def spdk_process_start(self, spdk_cpu_mask, spdk_mem):
        params = {
            "spdk_cpu_mask": spdk_cpu_mask,
            "spdk_mem": spdk_mem}
        return self._request("POST", "spdk_process_start", params)

    def join_swarm(self, cluster_ip, join_token, db_connection):
        params = {
            "cluster_ip": cluster_ip,
            "join_token": join_token,
            "db_connection": db_connection}
        return self._request("POST", "join_swarm", params)

    def spdk_process_kill(self):
        return self._request("GET", "spdk_process_kill")

