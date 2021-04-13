
# Pyjailgolf_2
## Description:
<div class="challenge-description">Now you have 9 characters to get the flag. Good luck!<br/>
<br/>
nc chal.b01lers.com 1335<br/>
<div class="bbcode_code">
<div class="bbcode_code_head">Code:</div>
<div class="bbcode_code_body" style="white-space:pre">line = input('&gt;&gt;&gt; ')

flag="[REDACTED]"

if len(line) &gt; 9:
    raise Exception()

try:
    eval(line)
except:
    pass</div>
</div>
<br/>
<i>by nsnc</i></div>

