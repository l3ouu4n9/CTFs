
# Virtual_Machine_Monitor_UWU
## Description:
A botnet has infected your computer. By examining the URL of its command and control server, you've discovered that your backup server is co-resident with the command and control server. You decided to prime and probe the instruction set cache of the VM to determine the botnets secret key and shut it down. You now have a collection of cache vectors representing the response time of the shared instruction cache. Your goal is to determine the key. Luckily, your hosting provider is antiquated and the botnet VM doesn't alternate between cores so you could continuously monitor it. You also know that the victim VM uses the exponent by squaring algorithm in cryptographic operations with the key.

```
int mult(int x, int y) { return x * y; }

int div(int x, int y) { return x / y; }

int exp_by_squaring(int x, int n) {
  if (n == 0) {
    return 1;
  }
  int y = 1;
  while (n > 1) {
    if (n % 2 == 1) {
      x = pow(x, 2);
      n = div(n, 2);
    } else {
      y = mult(x, y);
      x = pow(x, 2);
      n = div((n - 1), 2);
    }
  }
  return x * y;
}
```


In your lab, you ran the same hardware as the target VM with a similar software stack. You used the same prime and probe technique to label cache vectors P, D, M referring to when the functions pow, div, mult were running. Below are the datasets from the machines.

[target.csv](/files/17c40af38b0d112dca5eb5cf75b420b7/target.csv)

[lab.csv](/files/ee07cfa696a1e52ef82f71a20c36e40e/lab.csv)

The flag is the n parameter of exp_by_squaring used by the victim VM in binary.


-- a1c3

