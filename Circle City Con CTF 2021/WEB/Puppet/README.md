
# Puppet
## Description:
<div class="challenge-description">The flag has a random name in ~/Documents<br/>
Pwn my browser &gt;:)<br/>
<div class="bbcode_code">
<div class="bbcode_code_head">Code:</div>
<div class="bbcode_code_body" style="white-space:pre">const browser = await puppeteer.launch({
  dumpio: true,
  args: [
    '--disable-web-security',
    '--user-data-dir=/tmp/chrome',
    '--remote-debugging-port=5000',
    '--disable-dev-shm-usage', // Docker stuff
    '--js-flags=--jitless' // No Chrome n-days please
  ]
})</div>
</div>
<br/>
Challenge: <a class="bbcode_url" href="http://35.225.84.51">http://35.225.84.51</a><br/>
<br/>
Author: qxxxb<br/>
</div>

