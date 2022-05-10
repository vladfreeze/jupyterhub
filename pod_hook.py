from .k8s_functions import make_volume
from .types import CustomSpawner
from tornado import gen

@gen.coroutine
def my_pod_hook(spawner: CustomSpawner, pod):
    spawner.log.info('### pod_hook')
    #make group volumes
    for claim in spawner.nfs_claims:
        try:
            yield make_volume(spawner, claim)
        except Exception as e:
            spawner.log.info('### Error: make_volume')
            spawner.log.error(e)
            pass
    raise gen.Return(pod)
