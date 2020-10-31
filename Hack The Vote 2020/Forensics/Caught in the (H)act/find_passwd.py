import re
from pandare import Panda

panda = Panda(generic='x86_64')
panda.load_plugin('asidstory')

panda.enable_memcb()
panda.run_replay('vote')