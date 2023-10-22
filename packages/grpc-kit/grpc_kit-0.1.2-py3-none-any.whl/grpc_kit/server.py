import logging
from concurrent import futures

import grpc

from grpc_kit.utils import find_services

DEFAULT_SERVER = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

logger = logging.getLogger('grpc_kit.server')


class RpcServer:
    register_servicers = {}

    @classmethod
    def add_servicer(cls, name, servicer):
        cls.register_servicers[name] = servicer

    def __init__(self, proto_module, server=None):
        self._server = server or DEFAULT_SERVER
        self._proto_module = proto_module
        self._proto = {}

    def start(self, port=5001):
        """
        :param port:
        :return:
        """
        self._proto = find_services(self._proto_module)
        for service_name, modules in self._proto.items():
            pb2_grpc_module = getattr(modules['pb2_grpc'], f'add_{service_name.capitalize()}ServiceServicer_to_server')
            pb2_grpc_module(self.register_servicers[service_name], self._server)
        self._server.add_insecure_port(f'[::]:{port}')
        self._server.start()
        logger.info(f"Server started. Listening on port 「{port}」.")
        self._server.wait_for_termination()
