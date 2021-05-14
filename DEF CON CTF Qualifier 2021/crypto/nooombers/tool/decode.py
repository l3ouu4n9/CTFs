import re


def multiple_replace(string, rep_dict):
    pattern = re.compile(
        "|".join([re.escape(k) for k in sorted(rep_dict, key=len, reverse=True)]),
        flags=re.DOTALL,
    )
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)


MAPPING = {}


def readmenu(f):
    menu = f.readline().strip()
    MAPPING[menu] = "menu"
    for i in range(11):
        choice = f.readline().strip()
        MAPPING[choice] = chr(ord("a") + i)
    prompt = f.readline().split(" ")[0]
    MAPPING[prompt] = ">"


def readnums(f):
    num_id = 1
    for l in f.readlines():
        if len(l) > 20:
            tok = [t for t in l.strip().split(" ") if len(t) > 20]
            for t in tok:
                if t not in MAPPING:
                    MAPPING[t] = f"num{num_id}"
                    num_id += 1


with open("interaction1.txt") as f:
    f.readline()
    f.readline()
    readmenu(f)
    readnums(f)
    for k,v in MAPPING.items():
        print(f'{v} -> {k}')

with open("interaction1.txt") as f:
    for l in f.readlines():
        print(multiple_replace(l, MAPPING), end="")
