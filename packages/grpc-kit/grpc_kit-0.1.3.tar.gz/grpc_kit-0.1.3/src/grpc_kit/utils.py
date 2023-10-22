import glob
import os
import types
from importlib import import_module
from typing import Union


def is_module(var):
    return isinstance(var, types.ModuleType)


def _import_module(proto_module, module_path):
    module_name = os.path.basename(module_path).split('.')[0]
    module = import_module(f'{proto_module}.{module_name}')
    return module


def get_service_name(module_path):
    module_name = os.path.basename(module_path).split('.')[0]
    return module_name.split('_')[0]


def find_services(proto_module: Union[str, types.ModuleType]) -> dict:
    """寻找所有的服务"""
    if not is_module(proto_module):
        proto_module = import_module(proto_module)
    proto = {}
    pd2_files = glob.glob(os.path.join(proto_module.__path__[0], '*_pb2.py'))
    pd2_grpc_files = glob.glob(os.path.join(proto_module.__path__[0], '*_pb2_grpc.py'))
    for pb2, pb2_grpc in list(zip(pd2_files, pd2_grpc_files)):
        proto[get_service_name(pb2)] = {
            'pb2': _import_module(proto_module.__spec__.name, pb2),
            'pb2_grpc': _import_module(proto_module.__spec__.name, pb2_grpc)
        }
    return proto
