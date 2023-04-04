import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run
import logging
import paramiko
from paramiko import BadHostKeyException
logging.basicConfig(level=logging.DEBUG)
#paramiko.util.log_to_file('demo.log')

look_for_keys = False
allow_agent = False

REPO_URL = 'https://github.com/benuflection/ToDoListProj'
#hardcoded user


env.hosts = ['mikde@raspberrypi:22']
#env.passwords = {'mikede@raspberrypi:22': 'shittyshitterson'}
env.passwords = {'mikede@192.168.1.9:22': 'shittyshitterson'}

def deploy():
        ####   env.user replaced with hardcoded "mikede" because user is different on testing computer and server
    try:
        site_folder = f'/home/{env.user}/sites/{env.host}'
        #######site_folder = f'/home/mikede/sites/{env.host}'
        run(f'mkdir -p {site_folder}')
        with cd(site_folder):
            _get_latest_source()
            _update_virtualenv()
            _create_or_update_dotenv()
            _update_static_files()
            _update_database()
    except Exception as e:
        print(f"Bad Host Key Exception: {e}")
    except Exception:
        print("Other Exception")
def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')

def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run(f'python -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')

def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')

def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput')