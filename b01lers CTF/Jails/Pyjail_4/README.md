
# Pyjail_4
## Description:
<div class="challenge-description">Pyjail challenges can only get so difficult they said.<br/>
<br/>
nc chal.b01lers.com 1337<br/>
<div class="bbcode_code">
<div class="bbcode_code_head">Code:</div>
<div class="bbcode_code_body" style="white-space:pre">import sys
line = sys.stdin.buffer.readline()
banned = b".()=+-/"
for char in banned:
    if char in line:
        print("Nope")
        break
else:
    print(eval(line, {'globals': {}, '__builtins__': {'getattr': getattr}}))</div>
</div>
<br/>
<i>by nsnc</i></div>

