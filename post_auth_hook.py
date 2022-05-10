import json
from .variables import *
from jupyterhub.auth import Authenticator

async def my_post_auth_hook(authenticator: Authenticator, handler, authentication):
    print('### POSTAUTH')

    # failsave auth_state
    if authentication['auth_state'] is None:
        print('## denied acces')
        authentication['auth_state'] = {}
        return authentication

    # set spawning environment
    authentication['auth_state']['user_name'] = authentication['name']
    authentication['auth_state']['auth_handler'] = 'DEFAULT'
    try:
        authentication['auth_state']['groups'] = authentication['auth_state']['oauth_user']['groups']
        authentication['auth_state']['auth_handler'] = 'OAUTH'
    except Exception as e:
        try:
            json_loaded = False
            try:
                groups = json.loads(authentication['auth_state'][course_name_key])
                groups = [groups] if (isinstance(groups, str)) else groups
                authentication['auth_state']['groups'] = groups
                json_loaded = True
            except Exception as e:
                pass
            if not json_loaded:
                authentication['auth_state']['groups'] = [authentication['auth_state'][course_name_key].replace('"', '').replace("'", '')]
            authentication['auth_state']['auth_handler'] = 'LTI'
        except Exception as e:
            authentication['auth_state']['groups'] = ['default']
            pass
    try:
        authentication['auth_state']['roles'] = authentication['auth_state']['oauth_user']['roles']
    except Exception as e:
        try:
            json_loaded = False
            try:
                roles = json.loads(authentication['auth_state'][role_key])
                roles = [roles] if (isinstance(roles, str)) else roles
                authentication['auth_state']['roles'] = roles
                json_loaded = True
            except Exception as e:
                pass
            if not json_loaded:
                authentication['auth_state']['roles'] = [authentication['auth_state'][role_key].replace('"', '').replace("'", '')]
        except Exception as e:
            authentication['auth_state']['roles'] = ['Learner']
            pass
    
    authentication['auth_state']['admin'] = True if authentication['admin'] or "Administrator, WU-ADMIN" in authentication['auth_state']['roles'] else False
    authentication['auth_state']['super_admin'] = True if authentication['admin'] or "sysad, jupyteradmin, WU-SUPERADMIN" in authentication['auth_state']['roles'] else False

    # debug
    print('### debug')
    for i in authentication:
        print(i + ': ' + str(authentication[i]))
    print('### debug end')

    return authentication
