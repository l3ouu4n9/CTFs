
# Pyjailgolf_3
## Description:
<div class="challenge-description">nc chal.b01lers.com 1338<br/>
<div class="bbcode_code">
<div class="bbcode_code_head">Code:</div>
<div class="bbcode_code_body" style="white-space:pre">line = input('&gt;&gt;&gt; ')
# Some code here to remove that function that you used to solve pyjailgolf 2 from builtins
# The only reason it is censored is to not spoil pyjailgolf 2.
builtins = [REDACTED]

flag="[REDACTED]"

if len(line) &gt; 10:
    raise Exception()

try:
    eval(line, {'__builtins__': builtins}, locals())
except:
    pass</div>
</div>
<br/>
<i>by nsnc</i></div>

