import inspect
import re

from grpc_kit import RpcServer
from grpc_kit.utils import find_services


def with_result(func):
    def wrapper(self, request, context):
        response_name = re.sub(r"Request$", "Response", request.DESCRIPTOR.name)
        result = func(self, request, context)
        return getattr(self.pb2, response_name)(**result)

    return wrapper


class Service:
    def __init__(self, proto_module):
        self._proto_module = proto_module

    def __call__(self, cls, **kwargs):
        for name, method in cls.__dict__.items():
            if callable(method):
                if 'request' in inspect.getfullargspec(method).args:
                    setattr(cls, name, with_result(method))

        name = cls.__name__
        rej = re.search(r'^(?P<name>\w+)Service', name)
        service_name = rej.groupdict().get("name", None)
        if not service_name:
            raise Exception("service name is not found")

        RpcServer.add_servicer(service_name.lower(), cls())
        cls._proto = find_services(self._proto_module)
        cls.pb2 = cls._proto[service_name.lower()].get("pb2")
        return cls

