import angr

p = angr.Project('./SSE_KEYGENME',  load_options = {'auto_load_libs': False})

state = p.factory.full_init_state(args=['./SSE_KEYGENME'], add_options=angr.options.unicorn, stdin=angr.SimFile)

sm = p.factory.simulation_manager(state)
sm.explore(find=[0x00400d48], avoid=[0x00400d56])

print(sm.found[0].posix.dumps(0))