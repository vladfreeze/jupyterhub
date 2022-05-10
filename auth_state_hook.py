import json
from .types import CustomSpawner
from .variables import *
from jinja2 import Template

# for selecting kernels and volumes USE THIS HOOK !!!!
def my_auth_state_hook(spawner: CustomSpawner, auth_state):
    spawner.log.info('### AUTHSTATE')
    profile_list = []
    try:
        with open('/etc/jupyterhub/custom/kernels.json', 'r') as kernel_f:
            kernels = json.load(kernel_f)
        spawner.admin = auth_state['admin']
        spawner.superadmin = auth_state['super_admin']
        spawner.roles = auth_state['roles']
        spawner.groups = auth_state['groups']
        spawner.auth_handler = auth_state['auth_handler']
        spawner.user_name = auth_state['user_name']
        spawner.default_profile = kernels['default']

        #TODO edit this with new api so only relevant courses are displayed
        if 'WU-STUDENT' in spawner.roles or 'WU-STAFF' in spawner.roles:
            for kernel in kernels:
                kernels[kernel]['key'] = kernel
                profile_list.append(kernels[kernel])
            spawner.wu = True
            spawner.profiles = profile_list
            with open('/etc/jupyterhub/custom/profile_form_template.j2', 'r') as template_f:
                template = Template(template_f.read().replace('\n',''))
                spawner.options_form = template.render(profile_list=profile_list, javascript=Template(javascript), style=Template(style), wu_user=True)
        else:
            spawner.wu = False
            # checks if user from idp is in group
            for kernel in kernels:
                kernels[kernel]['key'] = kernel
                for group in spawner.groups:
                    try:
                        if str(kernel) == str(group) or str(kernels[kernel]['slug']) == str(group):
                            profile_list.append(kernels[kernel])
                    except Exception as e:
                        spawner.log.info('### group error:')
                        spawner.log.error(e)
                        pass

            profile_list.append(kernels['default'])
            spawner.profiles = profile_list


            # pre select custom kernel if just one (+default) is available and skip selection
            if len(profile_list) <= 2:
                profile = profile_list[0]
                profile['default'] = True
                spawner.profiles = [profile]
                profile_list = [profile]
                spawner.user_options = {"profile": profile['slug']}
            else:
                with open('/etc/jupyterhub/custom/profile_form_template.j2', 'r') as template_f:
                    template = Template(template_f.read().replace('\n',''))
                    spawner.options_form = template.render(profile_list=profile_list, javascript=Template(javascript), style=Template(style), wu_user=False)

    except Exception as e:
        spawner.log.info('### AUTHSTATE ERROR:')
        spawner.log.info(profile_list)
        spawner.log.error(e)
