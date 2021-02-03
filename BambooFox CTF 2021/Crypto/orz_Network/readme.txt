Say hello to the newest orz network.

There are 420 computers in this network, labeled from #1 to #420.
For each pair of computers, there may be a secure connection between them.
Each connection was initialized with a Diffie-Hellman key exchange under a multiplicative group modulo some prime number.

Today you and your hacker friend are given a mission: hack into and control the entire orz network.

Your friend had already hacked into and gained access to computer #1.
If you have access to computer #A and have already hijacked the connection between computers #A and #B, then you can gain access to computer #B.
To hijack a connection, all you have to do is to steal that connection's shared secret key (from the key exchange).

However, the admins of orz network are very experienced, so you can only hijack at most 419 connections before getting caught.
If your attack takes over 5 seconds, then you'll also get caught.

Fortunately, you are given the details of all connections.
You speak to yourself, "Isn't this the classic graph algorithm problem that I've solved a million times?"
Well, yes. Find a list of 419 connections to hijack, so that you can gain access to every computer.
Complete the mission, and you will be awarded the flag.


Notice: timer starts *after* the server sends you all the logs. Generating logs may take a few seconds, please be patient.
