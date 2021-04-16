#!/usr/bin/env python3

from Crypto.Util.number import bytes_to_long, isPrime
from sympy import *

# dp and dq are from key_to_hex.py, searching for the first 2 028201 sequence
dp = 0xc0cfc776f9bcad7e90e82f00b582c0ffe26f5acc4bc465b89cbf3c76097ad515563f3e0f67358f350c1b7d6a216b2e7adbe71c4f114cd2b971b83a070e1ec0e17e395b4f8c0496dd6134a857316cd6bd5b8e83e9c019ec2f5a4d0240b9ce5a10154926be9cc10fa0da2d7d223a166daac89c8723c6132547d1162fd8bdd43d80217667986ec6dce91ba1bdaf6d55450c73e9c5c8a7f9d4eb38bc2f0c6139f261926aa3fe68011ef0b7af34e9996c4d0a3095b48f9f585882d4a46bf44afa00672b21619a2862fc9cb48093604ffa7f15bd43697eac8e74e93dbc5f1d75fd8f61310b7b87d7fd729c5d6da4b069d8037dfeb6dcd8dd8db4e2375b8a095f692b51

dq = 0x51c69153116a1f1c9664ec0e9e68bec093342d2645aa465ca8afb61dd7039075a8aa0dd3b6d006d649b9dbd7c9ac8861b03e6db921416a6b6d7850b0bceecad6341770e75fd6d17699886ce68eb72d7c7c19995510df53aea435af7b806eb410483adf6c1274eafa93220bdde73e9ac6fc4f2e04bc85d8a5ff73c58805afd6a44fe6982de5be0b5b3c2d8df65acd79a1cce103de46b7dc8f9daac71298228e795d41a93121a3114687893a9265ae50251dbab3943c39c795b2ae5f5040cf6f11c4869d085155476ab0c1936082d222febd0b28f364108e6d326c9d7fa68b0f35f0c79581eeaa1480ad5a11a44d78af533e1485ced12d3941f97644757c05d7c5

e = 0x10001

for kq in range(1, e):
    q_mul = dq * e - 1
    if q_mul % kq == 0:
        q = (q_mul // kq) + 1
        if isPrime(q):
        	print("Potential q: " + str(q))

for kp in range(1, e):
    p_mul = dp * e - 1
    if p_mul % kp == 0:
        p = (p_mul // kp) + 1
        if isPrime(p):
        	print("Potential p: " + str(p))

"""
Potential q: 24312821138947295842939811430266614164483390266044923887694157098746040509093637457237135603411011833287827123602619771315554896936017168546924189851322281151620644250524117043049673777703814283705410796690775974401304283378519985368125276766049671207507190418663428295243489814095988104136549989630636041063221268290523766428047760530245982382697752496455539057488593944136069627708927281633167017337393918797915410963972736328647804191560830879679674669676405585810075964267210384497030345823969704188597922024875674517047635080525199694836436149951817779893116507111781865061463859626764914849867030257100120765229
Potential p: 531728207659942301795253901084381737110883040097313053322913639565173847736026567062658310606998607620829538859271019692779574663546063949380410110347896571016088740644703155824678492122200126954702690666327960507428268541835210899166622764600001960907380213645069024205628211424497796451244548457631029653033974543275052835017313659168468855844022055884671115800091077092022099362967367260138515603050906837518856621847732055920780974661504255852004514803319931650360002033069998882446652627303752496381522697600057253746343547131595999387666854098155533978693698059492388066835684589123085776392908036740654319726890609
Potential p: 32155793883644309494149365087347710275210633774631897274003001908876018851960968012981271807389852904017267710405842990613181825323298497180721462889930852141756696942713059737825259562300443091116514916928396257101370860052927606384048304583938193088254729901128992755541135185322798527530512122498248043845789461978413935354215871986482151417756534584220556107891332673683000687165418919940645597668777626845600908432978474596080126672805046918964956144371065049005805638187590643592564866189148070656840995258832683463131564291944605671726345796937320632480267178246999762145360703260951002442725449730325007240379
"""