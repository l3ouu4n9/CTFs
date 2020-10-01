# Spy Cam
Oh no! I found some spyware on my laptop. Can you find out what the attacker saw? 

## Writeup
1. Open the pcap file with wireshark, we can see that there are jpg files transmitted in tcp stream.
2. With `foremost capture.pcap`, I got all the image files with flag segments on them.