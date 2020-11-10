import angr

p = angr.Project('./hotel_key_puzzle',  load_options = {'auto_load_libs': False})

state = p.factory.full_init_state(args=['./hotel_key_puzzle'], add_options=angr.options.unicorn, stdin=angr.SimFile)

sm = p.factory.simulation_manager(state)
sm.explore(find=[0x004022ba], avoid=[0x004022c8])

print(sm.found[0].posix.dumps(0))