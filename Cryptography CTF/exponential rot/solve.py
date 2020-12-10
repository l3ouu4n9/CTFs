alphabet = "abcdefghijklmnopqrstuvwxyz"
cipher = "wdjzkhy trsz paxwjvkkw zg aqc wgcow rtqngdo wm dsx!. sfb afty yh sxlq{kyeuxr_js_llp_nask_woep_afmhyidae}. wlqm lwthth elfnl ax itpm cqamhtd bdgf"
flag = ""
count = 0
for i in range(len(cipher)):
    if (cipher[i] in ['{','}','_',' ','!','.']):
        flag += cipher[i]
    else:
        flag += alphabet[(alphabet.index(str(cipher[i]))+count)%26]
    count += 1
print(flag)