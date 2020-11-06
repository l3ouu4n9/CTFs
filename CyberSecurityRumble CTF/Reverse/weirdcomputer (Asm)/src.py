#!/usr/bin/env python3
import random
import base64
print("Hello :)")
print("Press L for code, or do some magic stuff")
i = input("> ")
if i.strip() == "L":
    print(open(__file__, "r").read())
    exit()
try:
    ROM = base64.b64decode(i)
    PC = 0x0200
    I = 0x0000
    V = [0] * 16
    MEM = [0] * 4096
    STACK = 0x0EA0
    FB = 0x0F00
    for i, d in enumerate(bytes.fromhex("F0909090F02060202070F010F080F0F010F010F09090F01010F080F010F0F080F090F0F010204040F090F090F0F090F010F0F090F09090E090E090E0F0808080F0E0909090E0F080F080F0F080F08080")):
        MEM[i] = d
    start = random.randrange(2500, 3500)
    start += start%2
    for i, d in enumerate(open("/flag.txt","rb").read().strip()):
        MEM[start] = (0x1000 | start) >> 8
        MEM[start+1] = (0x1000 | start) & 0xff
        MEM[start + 2 + i] = d
    TIMER = 0x00
    SOUND = 0x00
    for i, d in enumerate(ROM):
        MEM[i+512] = d
    while PC < len(MEM)-1:
        high = MEM[PC]
        low = MEM[PC+1]
        instr = low + high * 256
        if instr == 0x00E0:
            for i in range(256):
                MEM[0x0F00 + i] = 0
        elif instr == 0x00EE:
            STACK-=2
            PC = MEM[STACK+1] + MEM[STACK] * 256
            continue
        elif instr>>12 == 1:
            if PC == (instr ^ 0x1000):
                print("endless loop detected, aborting. current framebuffer content:")
                for y in range(32):
                    print("".join(list([bin(p)[2:].rjust(8, "0") for p in MEM[FB+y*8:FB+y*8+8]])).replace("0", " ").replace("1", "\u2588"))
                break
            PC = instr ^ 0x1000
            continue
        elif instr>>12 == 2:
            MEM[STACK] = ((PC+2) >> 8)
            MEM[STACK+1] = ((PC+2) & 0xFF)
            STACK+=2
            PC = instr ^ 0x2000
            continue
        elif instr>>12 == 3:
            reg = instr>>8 & 0x0f
            val = instr & 0xff
            if V[reg] == val:
                PC += 2
        elif instr>>12 == 4:
            reg = instr>>8 & 0x0f
            val = instr & 0xff
            if V[reg] != val:
                PC += 2
        elif instr>>12 == 5:
            reg1 = instr>>8 & 0x0f
            reg2 = (instr >> 4) & 0x0f
            if V[reg1] == V[reg2]:
                PC += 2
        elif instr>>12 == 6:
            reg = instr>>8 & 0x0f
            val = instr & 0xff
            V[reg] = val
        elif instr>>12 == 7:
            reg = instr>>8 & 0x0f
            val = instr & 0xff
            V[reg] = (V[reg] + val) % 256
        elif instr>>12 == 8 and (instr & 0x0f) == 0:
            reg1 = instr>>8 & 0x0f
            reg2 = (instr >> 4) & 0x0f
            V[reg1] = V[reg2]
        elif instr>>12 == 8 and (instr & 0x0f) == 1:
            reg1 = instr>>8 & 0x0f
            reg2 = (instr >> 4) & 0x0f
            V[reg1] |= V[reg2]
        elif instr>>12 == 8 and (instr & 0x0f) == 2:
            reg1 = instr>>8 & 0x0f
            reg2 = (instr >> 4) & 0x0f
            V[reg1] &= V[reg2]
        elif instr>>12 == 8 and (instr & 0x0f) == 3:
            reg1 = instr>>8 & 0x0f
            reg2 = (instr >> 4) & 0x0f
            V[reg1] ^= V[reg2]
        elif instr>>12 == 8 and (instr & 0x0f) == 4:
            reg1 = instr>>8 & 0x0f
            reg2 = instr>>4 & 0x0f
            V[reg1] += V[reg2]
            if V[reg1] > 255:
                V[reg1] = V[reg1] % 256
                V[0xF] = 1
            else:
                V[0xF] = 0
        elif instr>>12 == 8 and (instr & 0x0f) == 5:
            reg1 = instr>>8 & 0x0f
            reg2 = instr>>4 & 0x0f
            V[reg1] -= V[reg2]
            if V[reg1] < 0:
                V[reg1] = V[reg1] % 256
                V[0xF] = 0
            else:
                V[0xF] = 1
        elif instr>>12 == 8 and (instr & 0x0f) == 6:
            reg1 = instr>>8 & 0x0f
            reg2 = (instr >> 4) & 0x0f
            V[0xF] = V[reg1] & 0x01
            V[reg1] >>= 1
        elif instr>>12 == 8 and (instr & 0x0f) == 7:
            reg1 = instr>>8 & 0x0f
            reg2 = (instr >> 4) & 0x0f
            V[0xF] = int(V[reg1] > V[reg2])
            V[reg1] = (V[reg2] - V[reg1]) % 256
        elif instr>>12 == 8 and (instr & 0x0f) == 0xE:
            reg1 = instr>>8 & 0x0f
            reg2 = (instr >> 4) & 0x0f
            V[0xF] = (V[reg1] >> 7) & 0x01
            V[reg1] = (V[reg1] << 1) % 256
        elif instr>>12 == 9:
            reg1 = instr>>8 & 0x0f
            reg2 = (instr >> 4) & 0x0f
            if V[reg1] != V[reg2]:
                PC += 2
        elif instr>>12 == 0xA:
            I = instr & 0xfff
        elif instr>>12 == 0xB:
            PC = (instr & 0xfff) + V[0]
        elif instr>>12 == 0xC:
            reg = instr>>8 & 0x0f
            val = instr & 0xff
            V[reg] = random.randrange(256) & val
        elif instr>>12 == 0xD:
            reg1 = instr>>8 & 0x0f
            reg2 = (instr >> 4) & 0x0F
            height = instr & 0xf
            X = V[reg1]
            Y = V[reg2]
            V[0xF] = 0
            for y in range(height+1):
                sprbyte = I + y
                for x in range(8):
                    if (X+x) > 63:
                        continue
                    fbbyte = FB + ( (Y+y) * 8 ) + (X+x)//8
                    newbit = int(bool(MEM[sprbyte] & (0x1 << (7-(x%8)))))
                    if newbit:
                        MEM[fbbyte] ^= newbit << (7 - (X+x) % 8)
                        V[0xF] = 1
        elif instr>>12 == 0xE:
            break
        elif instr>>12 == 0xF:
            reg = instr>>8 ^ 0xF0
            instr = instr & 0xFF
            if instr == 0x07:
                V[reg] = TIMER
            elif instr == 0x0A:
                break
            elif instr == 0x15:
                TIMER = V[reg]
            elif instr == 0x18:
                SOUND = V[reg]
            elif instr == 0x1E:
                I += V[reg]
                if I > 0xFFF:
                    V[0xF] = 1
                    I = I % 0xFFF
                else:
                    V[0xF] = 0
            elif instr == 0x29:
                I = V[reg] * 4
            elif instr == 0x33:
                MEM[I+0] = (V[reg] & 0xf00) >> 8
                MEM[I+1] = (V[reg] & 0x0f0) >> 4
                MEM[I+2] = (V[reg] & 0x00f)
            elif instr == 0x55:
                for i in range(reg+1):
                    MEM[I+i] = V[i]
            elif instr == 0x65:
                for i in range(reg+1):
                    V[i] = MEM[I+i]
            else:
                break
        else:
            break
        PC += 2
except:
    raise