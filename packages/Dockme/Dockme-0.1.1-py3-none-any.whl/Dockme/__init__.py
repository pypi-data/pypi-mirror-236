version = "0.1.1"


def hello():
    print('Hello from Dockme in Version:', version)


def get_version():
    print('Version:', version)



from .get_image import get_image
from .run_container import run_container
from .stop_container import stop_container
from .delet_container import delet_container
from .delet_image import delet_image
from. run_command_in_con import run_command



__all__ = ['get_image', 'run_container', 'stop_container', 'delet_container', 'delet_image', 'run_command']