import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run
import logging

#env.user = 'mikede'
print(env.user)
print(env.host)
print(SITENAME)