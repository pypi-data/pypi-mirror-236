version = "0.0.8"


def hello():
    print('Hello from Dockme in Version:', version)






from .get_image import get_image
from .run_container import run_container
from .stop_container import stop_container
from .delet_container import delet_container



__all__ = ['get_image', 'run_container', 'stop_container', 'delet_container']