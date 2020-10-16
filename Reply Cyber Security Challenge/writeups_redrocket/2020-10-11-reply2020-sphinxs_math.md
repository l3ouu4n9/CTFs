---
layout: post
category: coding
title: replyCTF 2020 - Sphinx's math
tags:
    - LevitatingLion
---

In this challenge we had to write a script to automatically solve a system of linear equations. We can do that by parsing each equation into a vector of coefficients from the left-hand side of the equation, and a result scalar from the right-hand side of the equation. After parsing every equation, we stack the coefficient vectors to obtain the coefficient matrix $A$ and we stack the result scalars to obtain the result vector $b$. The system of equations is then equivalent to $Ax=b$, where $x$ is a vector of the variables. Using numpy we obtain a solution, which we then insert into the left-hand side of the final formula by computing the dot product of its coefficient vector and the solution vector, to obtain the final result.

After repeating this 512 times, the server hands us the flag.

Flag: `{FLG:F0r63t_7h3_4r4b1c-num3r4l5_hi3r06lyph5_w1ll_n3v3r-d13!}`

```py
import string
import numpy as np
from requests_html import HTMLSession


def convert(s):
    print("convert:", s)
    return float(eval(s))


def solve(r):
    print(r.text)

    all_text = "".join(p.text for p in r.html.find("div.enigma>p"))

    variables = list(set(x for x in all_text if x not in string.printable))
    print(variables)

    mat_a = []
    vec_b = []
    num_eqs = 0
    for p in r.html.find("div.enigma>p"):
        print("equation:", p.text)
        eq, res = p.text.split("=")
        eq = eq.strip()
        res = res.strip()

        facs = {}
        fac = ""
        for c in eq:
            if c in variables:
                facs[c] = fac
                fac = ""
            else:
                fac += c

        facs = [(convert(facs[var]) if var in facs else 0.0) for var in variables]
        print("factors:", facs)

        if res == "?":
            print("num_eqs:", num_eqs)
            print("num_vars:", len(variables))
            print("result:")
            mat_a = np.reshape(mat_a, (num_eqs, len(variables)))
            vec_b = np.reshape(vec_b, (num_eqs,))
            print(mat_a)
            print(vec_b)
            print("sol:")
            x = np.linalg.lstsq(mat_a, vec_b, rcond=None)[0]
            print(x)

            print("final result:")
            final = np.dot(x, facs)
            print(final)
            final = int(round(final))
            print(final)

            r = sess.post(
                "http://codingbox4sm.reply.it:1338/sphinxsEquaji/answer",
                data={"answer": str(final)},
            )
            return r

        else:
            num_eqs += 1
            res = convert(res)
            print("res:", res)

            mat_a.append(facs)
            vec_b.append(res)


sess = HTMLSession()
r = sess.get("http://codingbox4sm.reply.it:1338/sphinxsEquaji/")
while True:
    r = solve(r)
```
