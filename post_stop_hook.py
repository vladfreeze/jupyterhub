from .k8s_functions import remove_k8s
from .variables import *
from .types import CustomSpawner

def my_post_stop_hook(spawner: CustomSpawner):
    #spawner.log.info('### start post_stop_hook')
    remove_k8s(spawner.pod_name)
