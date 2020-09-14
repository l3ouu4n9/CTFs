import angr, claripy


base_addr = 0x100000
target = angr.Project('welcome', auto_load_libs=False, main_opts={'base_addr': base_addr})
input_len = 16
STDIN_FD = 0

# Create bit vectors
flag_chars = [claripy.BVS('flag_%d' %i, 8) for i in range(input_len)]
flag = claripy.Concat(*flag_chars + [claripy.BVV(b'\n')])



# Construct Initial Program State
st = target.factory.full_init_state(args=["./welcome"], stdin=flag)

# Constrains
for k in flag_chars:
    st.solver.add(k < 0x3a)
    st.solver.add(k > 0x2f)

simgr = target.factory.simulation_manager(st)
find_addr  = 0x10165d # SUCCESS
avoid_addr = [0x101682, 0x101670] # FAILURE
simgr.explore(find=find_addr, avoid=avoid_addr)

if (len(simgr.found) > 0):
    for found in simgr.found:
        print(found.posix.dumps(STDIN_FD))
