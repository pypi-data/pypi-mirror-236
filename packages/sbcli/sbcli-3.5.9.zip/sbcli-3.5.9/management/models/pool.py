# coding=utf-8

from typing import List

from management import utils
from management.models.base_model import BaseModel


class Pool(BaseModel):

    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"

    attributes = {
        "pool_name": {"type": str, 'default': ""},
        "id": {"type": str, 'default': ""},
        "users": {"type": List[str], 'default': []},
        "groups": {"type": List[str], 'default': []},
        "pool_max_size": {"type": int, 'default': 0},
        "lvol_max_size": {"type": int, 'default': 0},
        "lvols": {"type": List[str], 'default': []},
        "status": {"type": str, 'default': ""},
        "secret": {"type": str, 'default': ""},

        "max_r_iops": {"type": int, 'default': 0},
        "max_w_iops": {"type": int, 'default': 0},

        "max_rw_ios_per_sec": {"type": int, 'default': 0},
        "max_rw_mbytes_per_sec": {"type": int, 'default': 0},
        "max_r_mbytes_per_sec": {"type": int, 'default': 0},
        "max_w_mbytes_per_sec": {"type": int, 'default': 0},
    }

    def __init__(self, data=None):
        super(Pool, self).__init__()
        self.set_attrs(self.attributes, data)
        self.object_type = "object"

    def get_id(self):
        return self.id

    def get_clean_dict(self):
        data = super(Pool, self).get_clean_dict()
        data['pool_max_size'] = utils.humanbytes(data['pool_max_size'])
        data['lvol_max_size'] = utils.humanbytes(data['lvol_max_size'])
        return data

    def has_qos(self):
        return 0 < (self.max_rw_ios_per_sec + self.max_rw_mbytes_per_sec + self.max_r_mbytes_per_sec + self.max_w_mbytes_per_sec)
