
# Noparensjail
## Description:
<div class="challenge-description">If you need to call a function in python, you use parentheses. And if you assign a value, you use an equal sign. Right?<br/>
<br/>
nc chal.b01lers.com 1336<br/>
<div class="bbcode_code">
<div class="bbcode_code_head">Code:</div>
<div class="bbcode_code_body" style="white-space:pre">line = input('&gt;&gt;&gt; ')

blacklist = "()="
for item in blacklist:
    if item in line.lower():
        raise Exception()

exec(line)</div>
</div>
<br/>
<i>by nsnc</i></div>

