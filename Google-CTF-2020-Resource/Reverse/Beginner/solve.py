import angr, claripy


target = angr.Project('a.out', auto_load_libs=False)
input_len = 15

# Create bit vectors
flag_chars = [claripy.BVS('flag_%d' %i, 8) for i in range(input_len)]
flag = claripy.Concat(*flag_chars + [claripy.BVV(b'\n')])


# Construct Initial Program State
st = target.factory.full_init_state(args=["./a.out"], stdin=flag)

# Constrains
for k in flag_chars:
    st.solver.add(k < 0x7f)
    st.solver.add(k > 0x20)


sm = target.factory.simulation_manager(st)
sm.run()
y = []
for x in sm.deadended:
    if b"SUCCESS" in x.posix.dumps(1):
        y.append(x)

#grab the first ouptut
valid = y[0].posix.dumps(0)
print(valid)
