
# worm_2
## Description:
<div class="challenge-description">An unintended solution for worm was found. This challenge is a patched version, and the only difference is this line:
<div class="bbcode_code">
<div class="bbcode_code_head">Code:</div>
<div class="bbcode_code_body" style="white-space:pre">exec su user1 -c "$cmd" 0&lt;&amp;-</div>
</div>
<br/>
Server:
<div class="bbcode_code">
<div class="bbcode_code_head">Code:</div>
<div class="bbcode_code_body" style="white-space:pre">nc 35.188.197.160 1002</div>
</div>
<br/>
Author: qxxxb</div>

