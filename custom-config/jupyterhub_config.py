
from jupyterhub.auth import DummyAuthenticator
from jupyterhub.auth import Authenticator
from jinja2 import Template
import json
from dockerspawner import DockerSpawner

c= get_config()
async def my_post_auth_hook(authenticator: Authenticator, handler, authentication):
    
    authentication['groups']= ["test_course:instructor","test_course2:instructor","test_course:student","test_course2:student"]

    roles_list = []
    for groupname in authentication['groups']:
        if ":" in groupname:
            if groupname.split(":")[-1] == 'instructor':
                role = {"name":groupname,"scopes": ['admin-ui',"list:users!group=" + ":".join(groupname.split(":")[:-1]) + ":student", 
                            "list:users!group=" + ":".join(groupname.split(":")[:-1]) +":instructor",
                            "groups!group=" + ":".join(groupname.split(":")[:-1]) +":student",
                            "groups!group=" + ":".join(groupname.split(":")[:-1]) +":instructor",
                            "read:servers!group=" + ":".join(groupname.split(":")[:-1]) +":student",
                            "read:servers!group=" + ":".join(groupname.split(":")[:-1]) +":instructor",
                            "access:servers!group=" + ":".join(groupname.split(":")[:-1]) +":student",
                            "access:servers!group=" + ":".join(groupname.split(":")[:-1]) +":instructor"],
                            "groups": [groupname]}
                roles_list.append(role)
    authentication['roles'] = roles_list 
    return authentication





options_form_tpl = """
<label for="image">Image</label>
<input name="image" class="form-control" placeholder="the image to launch (default: {default_image})"></input>
"""


def get_options_form(spawner):
    return options_form_tpl.format(default_image=spawner.image)

class CustomDockerSpawner(DockerSpawner):
    def options_from_form(self, formdata):
        options = {}
        image_form_list = formdata.get("image", [])
        if image_form_list and image_form_list[0]:
            options["image"] = image_form_list[0].strip()
            self.log.info(f"User selected image: {options['image']}")
        return options

    def load_user_options(self, options):
        image = options.get("image")
        if image:
            self.log.info(f"Loading image {image}")
            self.image = image

c.Application.log_level = 'DEBUG'

c.JupyterHub.template_paths = ['/usr/local/share/jupyterhub/templates/']
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DockerSpawner.options_form = get_options_form
c.JupyterHub.spawner_class = CustomDockerSpawner



c.DummyAuthenticator.admin_users= ["testadmin"]
c.DummyAuthenticator.refresh_pre_spawn = True
c.DummyAuthenticator.manage_groups = True
c.DummyAuthenticator.manage_roles = True

c.JupyterHub.ip = "127.0.0.1"
c.JupyterHub.hub_ip = "0.0.0.0"
c.DockerSpawner.image = "ghcr.io/austriandatalab/aocc_openscience_mage:sha-55e857d"
c.DockerSpawner.network_name = "jupyterhub"
c.DockerSpawner.remove = True
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": "/home/jovyan/work"}
c.DockerSpawner.http_timeout = 300
  ####################
  ### CUSTOM HOOKS ###
  ####################

c.DummyAuthenticator.post_auth_hook = my_post_auth_hook



