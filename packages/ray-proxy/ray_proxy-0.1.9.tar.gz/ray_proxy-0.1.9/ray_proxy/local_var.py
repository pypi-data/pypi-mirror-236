import atexit
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID

from ray_proxy import IRemoteInterpreter
from ray_proxy.py_environment import PyInterpreter
from ray_proxy.var_interface import IVar

T = TypeVar("T")


@dataclass
class LocalVar(Generic[T], IVar):
    # Locally placed var that behave like a RemoteVar
    env: PyInterpreter
    id: UUID

    def __post_init__(self):
        assert isinstance(self.id, UUID)
        self.___proxy_dirs___ = None
        self.released = True
        atexit.register(self.__atexit__)

    def __atexit__(self):
        if not self.released:
            self.env.decr_ref_id(self.id)
            self.released = True

    def __del__(self):
        if not self.released:
            self.env.decr_ref_id(self.id)
            self.released = True
            atexit.unregister(self.__atexit__())
            self.deleted = True

    def fetch(self):
        return self.env.fetch_id(self.id)

    def fetch_ref(self):
        pass

    def _remote_attr(self, item):
        pass

    def __getattr__(self, item):
        pass

    def __call__(self, args, kwargs):
        pass

    def __getitem__(self, item):
        pass

    def __setitem__(self, item, value):
        pass

    def __iter__(self):
        pass

    def ___call_method___(self, method, args, kwargs):
        pass

    def ___call_operator___(self, operator, args):
        pass

    def ___call_left_operator___(self, operator, arg):
        pass

    def ___call_right_operator___(self, operator, arg):
        pass

    def __add__(self, other):
        pass

    def __radd__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __rmul__(self, other):
        pass

    def __mod__(self, other):
        pass

    def __rmod__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __rtruediv__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __rsub__(self, other):
        pass

    def __bool__(self):
        pass

    def __type__(self):
        pass

    def __len__(self):
        pass

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __neg__(self, other):
        pass

    def __await__(self):
        pass
