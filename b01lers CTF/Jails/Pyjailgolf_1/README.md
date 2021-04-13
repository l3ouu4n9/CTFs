
# Pyjailgolf_1
## Description:
<div class="challenge-description">You have 10 characters to get the flag. Have fun!<br/>
<br/>
nc chal.b01lers.com 1334<br/>
<div class="bbcode_code">
<div class="bbcode_code_head">Code:</div>
<div class="bbcode_code_body" style="white-space:pre">line = input('&gt;&gt;&gt; ')

flag="[REDACTED]"

if len(line) &gt; 10:
    raise Exception()

try:
    eval(line)
except:
    pass</div>
</div>
<br/>
<i>by nsnc</i></div>

