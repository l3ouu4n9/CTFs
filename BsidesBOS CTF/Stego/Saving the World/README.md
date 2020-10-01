# Saving the World
Sometimes I dream of saving the world. Saving everyone from the invisible hand, the one that brands us with an employee badge, the one the forces us to work for them, the one that controls us every day without us knowing it. But I can't stop it. I'm not that special. I'm just anonymous. I'm just alone. 

## Writeup
The numbers in the middle of the image is the key. The decoding method is some kind of ROT cipher, witch `1=n, 2=o, ... 26=m`.

It can be decoded to 
```
so much depends
upon
a red wheel
barrow
glazed with rain
water
beside the white
chickens
the password is
twellicklosescto
```
Run `steghide extract -sf menu.jpg` with passphrase `twellicklosescto`, and got `flag.txt`.