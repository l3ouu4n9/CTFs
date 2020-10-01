# Sea Shells
Can you collect all the shells? 
<br>
<br>
## Writeup
There is no protection for this binary, and it leaks the address of the buffer.

The stack overflow payload is `shellcode + paddings + buffer_address`, so RIP will be the address of the buffer address, and we got our shellcode executed.