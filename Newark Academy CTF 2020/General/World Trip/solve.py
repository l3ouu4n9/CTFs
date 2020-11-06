from opencage.geocoder import OpenCageGeocode

key = ""
geocoder = OpenCageGeocode(key=key)

world = []
datas = open("enc.txt").read()
datas = datas.split(')')[:-1]
for data in datas:
    a, b = data.strip('(').split(',')
    world.append((float(a), float(b)))

flag = "nactf{"
for place in world:
    results = geocoder.reverse_geocode(place[0], place[1])
    flag += results[0]["components"]["country"][0]
else:
    flag+="}"
    print(flag)
