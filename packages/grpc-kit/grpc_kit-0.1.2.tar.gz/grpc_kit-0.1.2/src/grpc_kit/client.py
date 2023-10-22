import grpc

from grpc_kit.utils import find_services


class RpcClient:

    def __init__(self, _proto_module, target):
        self._proto_module = _proto_module
        self._proto = find_services(self._proto_module)
        self.channel = grpc.insecure_channel(target)

    def __call__(self, service_name: str, method_name: str, **kwargs):
        pb2 = self._proto[service_name]['pb2']
        pb2_grpc = self._proto[service_name]['pb2_grpc']

        stub = getattr(pb2_grpc, f"{service_name.capitalize()}ServiceStub")(self.channel)
        request = getattr(pb2, f"{method_name}Request")(**kwargs)
        response = getattr(stub, method_name)(request)
        return response
