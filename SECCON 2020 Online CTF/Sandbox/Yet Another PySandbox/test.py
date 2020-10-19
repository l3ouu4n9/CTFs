f = lambda x: x
type_code = type(f.func_code)

consts = (None,)
variables = ("ev" + "al",)
args = ("s",)

fake_code = ""
fake_code += "\x74" + "\x00\x00" # LOAD_GLOBAL(0)
fake_code += "\x7c" + "\x00\x00" # LOAD_FAST(0)
fake_code += "\x83" + "\x01\x00" # CALL_FUNCTION(1)
fake_code += "\x53"              # RETURN_VALUE
f.func_code = type_code(
    1,           # argcount      
    1,           # nlocals
    2,           # stacksize
    67,          # flags
    fake_code,   # bytecode
    consts,      # constants
    variables,   # local variables
    args,        # arguments
    "nyanta.py", # filename
    "neko_func", # objet name
    114514,      # line number
    "?"          # nazo
)

print(f("1+1"))