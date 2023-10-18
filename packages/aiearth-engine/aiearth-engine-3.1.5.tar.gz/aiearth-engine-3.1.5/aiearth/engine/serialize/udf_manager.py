import hashlib
# import inspect
import json
import pickle
from aiearth.core import g_var

import logging

from aiearth.core.client.client import BaseClient
from aiearth.core.client.endpoints import Endpoints
from aiearth.core.error import AIEError
from oss2 import StsAuth, Bucket
from tqdm import tqdm

from aiearth.engine.serialize import inspect
from aiearth.engine.udf_base.annotation import annotation_parser

log_lvl = 'INFO'
if g_var.has_var(g_var.GVarKey.Log.LOG_LEVEL):
    log_lvl = g_var.get_var(g_var.GVarKey.Log.LOG_LEVEL).upper()
logging.basicConfig(level=log_lvl)
logger = logging.getLogger(__name__)

IMPORTS = """
from aiearth.engine.udf_base.aie_udf_base import *
from aiearth.engine.udf_base.aie_udaf_base import AIEUDAF
from aiearth.engine.udf_base.annotation import *
from aiearth.engine.udf_base.images import *
"""


class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""

    def __init__(self, desc: str = None):
        super().__init__(unit='B', unit_divisor=1024, miniters=1, unit_scale=True, desc=desc)

    def update_to(self, byte_consumed, total_bytes):
        if total_bytes is not None:
            self.total = total_bytes
        return self.update(byte_consumed - self.n)  # also sets self.n = b * bsize


def convert_to_bytes(obj):
    # 将对象转换为字节流
    byte_stream = pickle.dumps(obj)

    return byte_stream


def calculate_md5(obj_bytes):
    # 计算MD5哈希值
    md5_hash = hashlib.md5()
    md5_hash.update(obj_bytes)
    md5_value = md5_hash.hexdigest()

    return md5_value


def get_source(udf_class):
    func_source = inspect.getsource(udf_class)
    return IMPORTS + func_source


def get_meta(source):
    return annotation_parser(source)


def manage(udf_class):
    # get md5 from func
    func_source: str = get_source(udf_class)
    func_uuid = calculate_md5(bytes(func_source, encoding='utf-8'))
    udf_name = udf_class.__name__

    resp = BaseClient.get(f"{Endpoints.HOST}/mariana/openapi/oss/getUdfStsToken?uuid={func_uuid}", {})
    if resp.status_code != 200:
        raise AIEError(10000000, f"注册{udf_name}时遇到了错误: {resp.content.decode(encoding='utf-8')}")
    result = json.loads(resp.content.decode(encoding='utf-8'))
    success = result['success']
    if not success:
        if result['code'] == 24240405:
            # udf 已经上传完成
            return func_uuid
        raise AIEError(10000000, f'注册{udf_name}时遇到了错误: {result["message"]}')
    logger.info(f'Registering UDF {udf_name}')
    module = result['module']
    if not isinstance(module, list) or len(module) < 2:
        raise AIEError(10000000, f"注册{udf_name}时遇到了错误: {resp.content.decode(encoding='utf-8')}")
    pickle_file_key_sts = module[0]
    meta_file_key_sts = module[1]

    auth1 = StsAuth(access_key_id=pickle_file_key_sts['accessKeyId'],
                    access_key_secret=pickle_file_key_sts['accessKeySecret'],
                    security_token=pickle_file_key_sts['securityToken'])
    bucket1 = Bucket(auth=auth1, endpoint=pickle_file_key_sts['endpoint'], bucket_name=pickle_file_key_sts['bucket'],
                     region=pickle_file_key_sts['region'])
    with TqdmUpTo(desc=f"Registering Func...") as t:
        bucket1.put_object(pickle_file_key_sts['fileKey'], func_source, progress_callback=t.update_to)
        t.total = t.n

    auth2 = StsAuth(access_key_id=meta_file_key_sts['accessKeyId'],
                    access_key_secret=meta_file_key_sts['accessKeySecret'],
                    security_token=meta_file_key_sts['securityToken'])
    bucket2 = Bucket(auth=auth2, endpoint=meta_file_key_sts['endpoint'], bucket_name=meta_file_key_sts['bucket'],
                     region=meta_file_key_sts['region'])
    with TqdmUpTo(desc=f"Registering Meta...") as t:
        bucket2.put_object(meta_file_key_sts['fileKey'], get_meta(func_source), progress_callback=t.update_to)
        t.total = t.n

    return func_uuid
