from PIL import Image

with open('red.txt', 'r') as file:
    r = [int(s) for s in file.readline().split()]
with open('green.txt', 'r') as file:
    g = [int(s) for s in file.readline().split()]
with open('blue.txt', 'r') as file:
    b = [int(s) for s in file.readline().split()]
with open('wires/v.txt', 'r') as file:
    v = [int(s) for s in file.readline().split()]
with open('wires/h.txt', 'r') as file:
    h = [int(s) for s in file.readline().split()]

print(len(r))
print(len(g))
print(len(b))
print(len(v))
print(len(h))
print(r)


c = 0
for I in range(40):
    Image0 = Image.new('RGB', (528, 315))
    pixels = Image0.load()
    for j in range(315):
        for i in range(528):
            pixels[i, j] = (r[c], g[c], b[c])
            c += 1

    Image0.show()

