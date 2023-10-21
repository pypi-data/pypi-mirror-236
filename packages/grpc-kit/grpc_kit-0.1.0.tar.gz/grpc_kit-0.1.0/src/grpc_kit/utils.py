import glob
import os
from importlib import import_module


def _import_module(proto_dir, module_path):
    module_name = os.path.basename(module_path).split('.')[0]
    module = import_module(f'{proto_dir}.{module_name}')
    return module


def get_service_name(module_path):
    module_name = os.path.basename(module_path).split('.')[0]
    return module_name.split('_')[0]


def find_services(proto_dir):
    """寻找所有的服务"""
    proto = {}
    pd2_files = glob.glob(os.path.join(proto_dir, '*_pb2.py'))
    pd2_grpc_files = glob.glob(os.path.join(proto_dir, '*_pb2_grpc.py'))
    for pb2, pb2_grpc in list(zip(pd2_files, pd2_grpc_files)):
        proto[get_service_name(pb2)] = {
            'pb2': _import_module(proto_dir, pb2),
            'pb2_grpc': _import_module(proto_dir, pb2_grpc)
        }
    return proto
