import os
import json
import requests
from .k8s_functions import setup_k8s
from .variables import *
from .types import CustomSpawner

def select_profile_group(spawner: CustomSpawner):
    spawner.log.info('### select_profile_group')
    selected_profile = Exception('Error select_profile_group')
    selected_group = Exception('Error select_profile_group')
    for profile in spawner.profiles:
        # legacy: for key entry based course definition instead of lv number as slug
        if str(spawner.user_options['profile']) == str(profile['slug']) or str(spawner.user_options['profile']) == profile['key']:
            selected_profile = profile
            selected_group = str(profile['key'])
            break

    return selected_profile, selected_group

def select_profile_by_wu_user(spawner: CustomSpawner):
    spawner.log.info('### select_profile_by_wu_user')
    try:
        selected_profile = Exception('not authorized')
        selected_group = Exception('not authorized')

        if str(spawner.user_options['profile']) in spawner.groups:
            spawner.log.info('### Group from keycloak')
            spawner.log.info(spawner.user_options)
            try:
                return select_profile_group(spawner)
            except Exception as e:
                spawner.log.error(e)
                pass

        #test if user is from wu:
        bach_url = bach_url_staff if 'WU-STAFF' in spawner.roles else bach_url_students

        wu_password = spawner.user_options['password'][0]
        spawner.log.info('### get user options')
        spawner.log.info(spawner.user_options)

        headers = {
            'Accept': '*/*'
        }
        r = requests.post(bach_url, headers=headers, auth=(spawner.user['name'], wu_password))
        data = r.json()
        for profile in spawner.profiles:
            if str(profile['slug']) == str(spawner.user_options['profile']):
                selected_profile = profile

        authorized = False
        # check if user has access to group
        for courses in data:
            if str(selected_profile['slug']) == str(courses[1]):
                selected_group = str(courses[1])
                authorized = True

        if authorized:
            return selected_profile, selected_group
        else:
            raise Exception('not authorized')

    except Exception as e:
        spawner.log.info('### authorize for group error, use defaults')
        spawner.log.error(e)
        return e


def get_user_profile_and_group(spawner: CustomSpawner):
    selected_profile = spawner.default_profile
    selected_group = 'default'

    if spawner.wu:
        try:
            selected_profile, selected_group = select_profile_by_wu_user(spawner)
        except Exception as e:
            spawner.log.info('### ERROR wu user')
            spawner.log.error(e)
            pass
    else:
        try:
            selected_profile, selected_group = select_profile_group(spawner)
        except Exception as e:
            spawner.log.info('### ERROR other user')
            spawner.log.error(e)
            pass

    return selected_profile, selected_group


def my_pre_spawn_hook(spawner: CustomSpawner):
    try:

        # init setup spawner vars
        spawner.log.info('### PRESPAWN')
        # get paths for mounting from nfs-crossmnt
        path = os.path.join(share_dirs)
        # spawner setup
        username = spawner.user_name
        is_admin = spawner.admin
        is_superadmin = spawner.superadmin
        escaped_servername = spawner._expand_user_properties('{servername}')
        escaped_username = spawner._expand_user_properties('{username}')
        spawner.pvc_name = 'claim-' + escaped_username

        # select correct profile
        selected_profile, selected_group = get_user_profile_and_group(spawner)
        nfs_claims = selected_profile["nfs_claims"]

        # setup pvcs, ingress and load balancer
        setup_k8s(spawner, nfs_claims)

        # spawner image setup
        spawner.image = selected_profile["image"]
        spawner.cpu_limit = selected_profile["cpu_limit"]
        spawner.mem_limit = selected_profile["mem_limit"]
        # Select default environment (lab/tree)
        try: 
            if selected_profile["default_url"] == '/tree':
                spawner.default_url = '/tree'
            else: 
                spawner.default_url = '/lab'
        except KeyError:
            print("No default_url set, applying global config")


        spawner.extra_labels = {
            'hub.jupyter.org/pod_name': spawner.pod_name,
            'hub.jupyter.org/network-access-hub':'true'
        }

        # add sidecars
        try:
            for sidecar in selected_profile['sidecars']:
                spawner.extra_containers.append(sidecar)
        except Exception as e:
            pass
        

        # Use same Home Directory for servers and users | spawner.name only when named server
        if len(spawner.name) > 0:
            spawner.volumes[0]["persistentVolumeClaim"]["claimName"] = 'claim-' + escaped_username
            spawner.volumes[0]['name'] = 'volume-' + escaped_username
            spawner.volume_mounts[0]["name"] = 'volume-' + escaped_username


        # see arg parsing of db_functions.py
        # -G group1 true -G group2 false -G group3 false
        # ==> [{'name': 'group1', 'is_admin': True}, {'name': 'group2', 'is_admin': False}, {'name': 'group3', 'is_admin': False}]
        init_dbs_command = ["python3", "/mnt/db_setup/db_functions.py", "-U", username, "-G", selected_group, str(is_admin)]
        dbs = [{"name":username, "is_admin": str(True)}, {"name":selected_group, "is_admin": str(is_admin)}]

        lecture_already_set = False
        for claim in nfs_claims:
            is_lecture = False

            try:
                is_lecture = claim['lecture']
                if lecture_already_set:
                    continue
                lecture_already_set = True
            except Exception as e:
                pass

            # see arg parsing of db_functions.py
            # -G group1 true -G group2 false -G group3 false
            # ==> [{'name': 'group1', 'is_admin': True}, {'name': 'group2', 'is_admin': False}, {'name': 'group3', 'is_admin': False}]
            if not is_lecture:
                init_dbs_command.append('-G')
                init_dbs_command.append(claim['name'])
                init_dbs_command.append(str(claim['writeable']))
                dbs.append({
                    "name": claim['name'],
                    "is_admin": str(claim['writeable'])
                })

            # setup mount_path    
            mount_path = default_group_share_dir_name if is_lecture else '/home/jovyan/' + claim['name']

            pvc = {
                'name': claim['name'],
                'persistentVolumeClaim': {
                    'claimName': claim['name'],
                    'storageAccessModes': 'ReadOnlyMany'
                }
            }
            mount = {
                'name': claim['name'],
                'mountPath': mount_path,
                'subPath': '',
                'readOnly': True
            }

            if (claim["storage_class"] is storage_class_sharedirs and (claim['writeable'] or (is_admin or is_superadmin))):
                # change default_share_claim to crossmnt_claim to enable write on default_share_claim
                spawner.volumes[1]["persistentVolumeClaim"]["storageAccessModes"] = 'ReadWriteMany'
                spawner.volumes[1]["persistentVolumeClaim"]["claimName"] = crossmnt_claim_name
                for dir in os.listdir(path):
                    if claim['name'] in dir:
                        mount['subPath'] = 'share_dirs/' + dir
                        mount['name'] = 'default'
                        mount['readOnly'] = False
                    if default_share_claim_name in dir:
                        spawner.volume_mounts[1]["subPath"] = 'share_dirs/' + dir
            elif (claim['writeable'] or (is_admin or is_superadmin)):
                pvc["persistentVolumeClaim"]["storageAccessModes"] = 'ReadWriteMany'
                mount["readOnly"] = False
                spawner.volumes.append(pvc)
            else:
                spawner.volumes.append(pvc)

            spawner.volume_mounts.append(mount)
            

        if (is_admin or is_superadmin):
            spawner.volume_mounts[1]["readOnly"] = False
            # change default_share_claim to crossmnt_claim to enable write on default_share_claim
            spawner.volumes[1]["persistentVolumeClaim"]["storageAccessModes"] = 'ReadWriteMany'
            spawner.volumes[1]["persistentVolumeClaim"]["claimName"] = crossmnt_claim_name
            for dir in os.listdir(path):
                if default_share_claim_name in dir:
                    spawner.volume_mounts[1]["subPath"] = 'share_dirs/' + dir
        if is_superadmin:
            # add user_path to crossmnt_claim to enable write on user_dirs
            spawner.volume_mounts.append({
                'name': 'default',
                'subPath': 'user_dirs/',
                'mountPath': default_user_dirs_name,
                'readOnly': False
            })


        # setup dbs init container
        spawner.init_containers = [{
            "name": "init-dbs",
            "image": "registry.ai.wu.ac.at/jupyter/images/init-dbs:latest",
            "command": init_dbs_command,
            "imagePullPolicy": "IfNotPresent",
            "volumeMounts": [{
                "name": "custom-config",
                "mountPath": "/mnt/db_setup"
            },{
                "name": "userdbsecrets",
                "mountPath": "/mnt/secrets",
                "readOnly": True
            }]
        }]

        # add db_functions.py and secrets for init-dbs container
        spawner.volumes.extend([{
            "name": "custom-config",
            "configMap": {
                "name": "custom-config",
                "items": [{
                    "key": "db_functions.py",
                    "path": "db_functions.py"
                }]
            }
        },{
            "name": "userdbsecrets",
            "secret": {
                "secretName": "userdbsecrets",
                "items": [{
                    "key": "mongo_url",
                    "path": "mongo_url"
                },{
                    "key": "postgresql_connect",
                    "path": "postgresql_connect"
                }]
            }
        }])


        try:
            # deduplicate volumes
            spawner.volumes = list({v['name']:v for v in spawner.volumes}.values())
            spawner.volume_mounts = list({v['mountPath']:v for v in spawner.volume_mounts}.values())
        except Exception as e:
            spawner.log.info('### Error Volumes Deduplication')
            spawner.log.error(e)
            pass

        try:
            # deduplicate sidecars
            spawner.extra_containers = list({v['name']:v for v in spawner.extra_containers}.values())
        except Exception as e:
            spawner.log.info('### Error extra_containers Deduplication')
            spawner.log.error(e)
            pass

        # add dbs to environment
        spawner.environment['DATABASES'] = json.dumps(dbs)
        spawner.environment['PGHOST'] = 'postgresql.student-db.svc.cluster.local'
        spawner.environment['PGUSER'] = username
        spawner.environment['PGPASSWORD'] = username

    except Exception as e:
        spawner.log.info('#### ERROR setting env:')
        spawner.log.error(e)
        pass











# bach fetch best case:
"""
    get_user_jupyter_lvs(username): ==> {
        list_of_jupyter_lvs: [
            {
                v_tid: NUMBER,
                verid: NUMBER,
                sem: STRING|NUMBER,
                is_admin: BOOLEAN
            },
            {...}
        ]
    }
"""
