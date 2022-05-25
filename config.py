import os

from jupyterhub.app import JupyterHub
from jupyterhub.handlers import BaseHandler
from oauthenticator.generic import GenericOAuthenticator
from .post_auth_hook import my_post_auth_hook
from .auth_state_hook import my_auth_state_hook
from .pre_spawn_hook import my_pre_spawn_hook
from .post_stop_hook import my_post_stop_hook
from .pre_spawn_hook import my_pre_spawn_hook
from .pod_hook import my_pod_hook

def setup_hub(c):

    c.Authenticator.refresh_pre_spawn = True
    c.Authenticator.auto_login = True
    c.Authenticator.auth_refresh_age = 600

    class LTI(LTIAuthenticator):
        consumers = {os.environ['LTI_CLIENT_KEY']: os.environ['LTI_CLIENT_SECRET']}

    class Keycloak(GenericOAuthenticator):
        login_service = "keycloak"
        client_id = os.environ['KEYCLOAK_CLIENT_ID']
        client_secret = os.environ['KEYCLOAK_CLIENT_SECRET']
        token_url = os.environ['OAUTH2_TOKEN_URL']
        userdata_url = os.environ['KEYCLOAK_CLIENT_userdata_url']
        userdata_method = "GET"
        userdata_params = {'state': 'state'}
        username_key = "preferred_username"
        authorize_url = os.environ['KEYCLOAK_CLIENT_authorize_url']

    c.MultiAuthenticator.keycloak_class = Keycloak
    c.MultiAuthenticator.lti_class = LTI

    c.Authenticator.post_auth_hook = my_post_auth_hook

    c.Spawner.start_timeout = 300

    c.KubeSpawner.auth_state_hook = my_auth_state_hook
    c.KubeSpawner.modify_pod_hook = my_pod_hook
    c.KubeSpawner.pre_spawn_hook = my_pre_spawn_hook
    c.KubeSpawner.post_stop_hook = my_post_stop_hook

    # setup arguments for the user spawner
    c.KubeSpawner.args = [
        "--FileCheckpoints.checkpoint_dir=/home/jovyan/.jupyter_checkpoints",
        "--NotebookApp.shutdown_no_activity_timeout=86400", #0 sekunden 86400=24h
        "--NotebookApp.iopub_data_rate_limit=500000000", #500000000
        "--NotebookApp.iopub_msg_rate_limit=3000", #3000
        "--NotebookApp.log_level=40", #40=Error 20=Info
        "--Application.log_level=40", #40=Error 20=Info
        "--JupyterApp.log_level=40", #40=Error 20=Info
        "--MappingKernelManager.cull_idle_timeout=10800", #10800 sekunden
        "--MappingKernelManager.cull_interval=1800", #1800 sekunden
        "--MappingKernelManager.buffer_offline_messages=False",
        "--GatewayKernelManager.cull_idle_timeout=10800", #10800 sekunden
        "--GatewayKernelManager.cull_interval=1800", #1800 sekunden
        "--GatewayKernelManager.buffer_offline_messages=False",
        "--TerminalManager.cull_inactive_timeout=10800", #10800 sekunden
        "--TerminalManager.cull_interval=1800" #1800 sekunden
    ]

    c.KubeSpawner.image_pull_secrets = "hub-image-credentials"
    c.KubeSpawner.pod_name_template = 'jupyter-{username}-{servername}'
    c.KubeSpawner.environment['MONGODB_HOSTNAME'] = 'mongodb.student-db.svc.cluster.local'
    c.KubeSpawner.environment['POSTGRESQL_HOSTNAME'] = 'postgresql.student-db.svc.cluster.local'
    c.KubeSpawner.k8s_api_request_retry_timeout = 120
    c.KubeSpawner.k8s_api_request_timeout = 10
    c.KubeSpawner.port = 8888
    c.KubeSpawner.extra_container_config = {
        "ports": [{
            "containerPort": 8888,
            "kind": "ClusterIP",
            "name": "notebook-port",
            "protocol": "TCP"
        }, {
            "containerPort": 8080,
            "kind": "ClusterIP",
            "name": "serve-web",
            "protocol": "TCP"
        }]
    }

    #c.JupyterHub.authenticator_class = "oauthenticator.generic.GenericOAuthenticator"
    #c.Authenticator.admin_users = {'vpopescu'}
    #c.Authenticator.refresh_pre_spawn = True
    #c.Authenticator.auto_login = True
    #c.Authenticator.enable_auth_state = True
 
  



    #c.Application.log_level = "DEBUG"


#

    #c.Authenticator.admin_users = {"vlad.popescu-vifor@wu.ac.at","vpopescu","thweber"}
    #c.Authenticator.post_auth_hook = my_post_auth_hook
    #c.KubeSpawner.auth_state_hook = my_auth_state_hook
    #c.KubeSpawner.modify_pod_hook = my_pod_hook
    #c.KubeSpawner.pre_spawn_hook = my_pre_spawn_hook
    #c.KubeSpawner.post_stop_hook = my_post_stop_hook
    ##


    
    