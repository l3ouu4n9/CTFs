with open("TJ.txt") as f:
    txt = f.read()

txt = txt.split(" ")
for i in range(len(txt)):
    if "tom" in txt[i]:
        txt[i] = txt[i].replace("tom","").replace("*","0")
    if "jry" in txt[i]:
        txt[i] = txt[i].replace("jry","").replace("*","1")
txt = "".join(txt).strip()
txt = "".join(chr(int(txt[i:i+8],2)) for i in range(0,len(txt),8))
txt = txt.replace(".","").replace(",","").replace("& ","").split(" ")
flag = "flag{" + "".join(s[0] for s in txt)+"}"
print(flag)