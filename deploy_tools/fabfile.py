from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run
import random


REPO_URL = 'git@github.com:DimitriiVasilev/testing_goat.git'


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('source/.git'):
        with cd('source'):
            run('git fetch')
    else:
        run(f'git clone {REPO_URL} source')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    with cd('source'):
        run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('venv/bin/pip'):
        run('python3.7 -m venv venv')
    run('./venv/bin/pip3 install -r source/requirements.txt')


def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_content = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_content:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')


def _update_static_files():
    run('./venv/bin/python3 source/manage.py collectstatic --noinput')


def _update_database():
    run('./venv/bin/python3 source/manage.py migrate --noinput')
