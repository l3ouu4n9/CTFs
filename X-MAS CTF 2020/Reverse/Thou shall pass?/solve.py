import angr, claripy

base_addr = 0x400000
target = angr.Project('thou_shall_pass', auto_load_libs=False, main_opts={'base_addr': base_addr})
input_len = 0x1f

# Create bit vectors
flag_chars = [claripy.BVS('flag_%d' %i, 8) for i in range(input_len)]
flag = claripy.Concat(*flag_chars + [claripy.BVV(b'\n')])


# Construct Initial Program State
st = target.factory.full_init_state(args=["./thou_shall_pass"], stdin=flag)

# Constrains
for k in flag_chars:
    st.solver.add(k < 0x7f)
    st.solver.add(k > 0x20)


simgr = target.factory.simulation_manager(st)
find_addr  = 0x401527 # SUCCESS
avoid_addr = 0x401535 # FAILURE
simgr.explore(find=find_addr, avoid=avoid_addr)

if (len(simgr.found) > 0):
    for found in simgr.found:
        inp = found.posix.dumps(0)
        if b'X-MAS' in inp:
            print(inp)